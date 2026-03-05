import logging
import time

from core.mt5_connector import MT5Connector
from core.prop_rule_engine import PropRuleEngine
from dto.LoginDTO import create_login_config
from firms.firm_profiles import get_firm_profile


def run_monitor(config: dict):
    """Main monitoring loop"""
    logger = logging.getLogger(__name__)

    # Load firm profile
    try:
        firm_profile = get_firm_profile(config['firm_key'])
    except KeyError as e:
        logger.error(str(e))
        return

    # Get login config (from config or environment)
    login_config = config['login_config']

    # Initialize MT5 connector
    logger.info("Connecting to MetaTrader 5...")
    if login_config:
        logger.info(f"Using login credentials: {login_config}")
    else:
        logger.info("Connecting to already running MT5 terminal...")

    mt5 = MT5Connector(
        login_config=login_config,
        magic_filter=config.get('magic_filter')
    )

    if not mt5.connect():
        logger.error("Failed to connect to MT5. Make sure MT5 is running.")
        return

    try:
        # Get initial account state
        account_state = mt5.get_account_state()
        if not account_state:
            logger.error("Failed to get account state")
            return

        # Use actual balance if starting_balance not provided
        starting_balance = config.get('starting_balance', account_state['balance'])

        # Initialize rule engine
        rule_engine = PropRuleEngine(firm_profile, starting_balance)

        logger.info("=" * 70)
        logger.info("  PROP FIRM CHALLENGE MONITOR STARTED")
        logger.info("=" * 70)
        logger.info(f"Firm: {firm_profile['name']}")
        logger.info(f"Starting Balance: ${starting_balance:.2f}")
        logger.info(f"Poll Interval: {config['poll_interval']}s")
        logger.info(f"Auto-close on breach: {config['auto_close_on_breach']}")
        logger.info("=" * 70)

        # Main monitoring loop
        iteration = 0
        last_status_print = time.time()

        while True:
            iteration += 1

            # Get current state
            account_state = mt5.get_account_state()
            if not account_state:
                logger.warning("Failed to get account state, retrying...")
                time.sleep(config['poll_interval'])
                continue

            open_positions = mt5.get_open_positions()
            closed_trades_today = mt5.get_closed_trades_today()

            # Check rules
            violation = rule_engine.check_rules(
                account_state,
                open_positions,
                closed_trades_today
            )

            # Handle violation
            if violation:
                logger.critical(f"🚨 RULE VIOLATION: {violation.value}")
                status = rule_engine.get_status_report(account_state)
                rule_engine.print_status(status)

                if config['auto_close_on_breach']:
                    logger.warning("Auto-closing all positions...")
                    successful, failed = mt5.close_all_positions()
                    logger.info(f"Closed {successful} positions, {failed} failed")

                logger.info("Monitoring stopped due to rule violation")
                break

            # Check if challenge passed
            if rule_engine.challenge_passed:
                logger.info("🎉 CHALLENGE PASSED!")
                status = rule_engine.get_status_report(account_state)
                rule_engine.print_status(status)
                logger.info("Monitoring stopped - challenge completed")
                break

            # Print status every 60 seconds
            if time.time() - last_status_print >= 60:
                status = rule_engine.get_status_report(account_state)
                rule_engine.print_status(status)
                last_status_print = time.time()

            # Quick log every iteration
            if iteration % 10 == 0:  # Every 10 iterations
                logger.debug(
                    f"[Check #{iteration}] "
                    f"Balance: ${account_state['balance']:.2f} | "
                    f"Equity: ${account_state['equity']:.2f} | "
                    f"Positions: {len(open_positions)}"
                )

            time.sleep(config['poll_interval'])

    except KeyboardInterrupt:
        logger.info("\n⚠️  Monitoring stopped by user")
        status = rule_engine.get_status_report(mt5.get_account_state())
        rule_engine.print_status(status)

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")

    finally:
        mt5.disconnect()
        logger.info("Disconnected from MT5")