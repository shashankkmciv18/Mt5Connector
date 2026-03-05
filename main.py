"""
Prop Firm Rule Monitor - Main Entry Point
Connects to MT5 and monitors prop firm challenge rules in real-time
"""
import argparse
import logging
import time
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.mt5_connector import MT5Connector
from core.prop_rule_engine import PropRuleEngine
from firms.firm_profiles import get_firm_profile, list_all_firms


# ============================================================================
# CONFIGURATION - Edit these settings
# ============================================================================
CONFIG = {
    'firm_key': 'funded_next_6k',           # Firm profile to use (see --list-firms)
    'starting_balance': 6000.0,             # Your challenge starting balance
    'magic_filter': None,                   # Filter by EA magic number (None = all trades)
    'auto_close_on_breach': False,          # Auto-close positions on rule breach
    'poll_interval': 1.0,                   # Check interval in seconds
    'log_level': 'INFO',                    # DEBUG, INFO, WARNING, ERROR
}


def setup_logging(log_level: str):
    """Setup logging configuration"""
    log_dir = Path(__file__).parent / 'logs'
    log_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f'prop_monitor_{timestamp}.log'

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Log file: {log_file}")
    return logger


def run_monitor(config: dict):
    """Main monitoring loop"""
    logger = logging.getLogger(__name__)

    # Load firm profile
    try:
        firm_profile = get_firm_profile(config['firm_key'])
    except KeyError as e:
        logger.error(str(e))
        return

    # Initialize MT5 connector
    logger.info("Connecting to MetaTrader 5...")
    mt5 = MT5Connector(magic_filter=config.get('magic_filter'))

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


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Prop Firm Challenge Rule Monitor',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--list-firms',
        action='store_true',
        help='List all available firm profiles'
    )

    parser.add_argument(
        '--firm',
        type=str,
        help='Firm profile key to use (overrides CONFIG)'
    )

    parser.add_argument(
        '--balance',
        type=float,
        help='Starting balance (overrides CONFIG)'
    )

    parser.add_argument(
        '--magic',
        type=int,
        help='Filter by EA magic number (overrides CONFIG)'
    )

    parser.add_argument(
        '--auto-close',
        action='store_true',
        help='Auto-close positions on rule breach'
    )

    parser.add_argument(
        '--interval',
        type=float,
        default=CONFIG['poll_interval'],
        help='Poll interval in seconds'
    )

    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default=CONFIG['log_level'],
        help='Logging level'
    )

    args = parser.parse_args()

    # Handle list-firms
    if args.list_firms:
        list_all_firms()
        return

    # Setup logging
    logger = setup_logging(args.log_level)

    # Override config with command line args
    config = CONFIG.copy()

    if args.firm:
        config['firm_key'] = args.firm
    if args.balance:
        config['starting_balance'] = args.balance
    if args.magic is not None:
        config['magic_filter'] = args.magic
    if args.auto_close:
        config['auto_close_on_breach'] = True
    if args.interval:
        config['poll_interval'] = args.interval

    # Run monitor
    try:
        run_monitor(config)
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
