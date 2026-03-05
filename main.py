"""
Prop Firm Rule Monitor - Main Entry Point
Connects to MT5 and monitors prop firm challenge rules in real-time
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import argparse
import logging

from datetime import datetime


from dto.LoginConfig import create_login_config
from firms.firm_profiles import list_all_firms
from monitor.PropFirmMonitor import run_monitor

# Add project root to path


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
    'login_config': create_login_config(732600,"123456789aA!","BlackBullMarkets-Demo")

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
