"""
MT5 Connector - Handles all MetaTrader 5 API interactions
"""
from siliconmetatrader5 import MetaTrader5
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging
import sys
from pathlib import Path

from dto.LoginDTO import LoginConfig

# Import LoginConfig DTO
sys.path.insert(0, str(Path(__file__).parent.parent))


logger = logging.getLogger(__name__)


class MT5Connector:
    """Manages connection and data retrieval from MT5 terminal"""

    def __init__(self, login_config: Optional[LoginConfig] = None, magic_filter: Optional[int] = None):
        """
        Initialize MT5 connector

        Args:
            login_config: LoginConfig DTO with MT5 credentials
            magic_filter: If provided, only monitor trades with this magic number
        """
        self.login_config = login_config
        self.magic_filter = magic_filter
        self.connected = False
        self.account_info = None
        self.mt5 = MetaTrader5(host="localhost", port=8001, keepalive=True)

    def connect(self) -> bool:
        """
        Connect to MT5 terminal

        Returns:
            True if connected successfully, False otherwise
        """
        if self.connected:
            return True
        # Initialize with login credentials if provided
        if self.login_config:
            if not self.mt5.initialize(
                login=self.login_config.login,
                password=self.login_config.password,
                server=self.login_config.server,
                timeout=self.login_config.timeout
            ):
                logger.error(f"MT5 initialize() failed, error code: {self.mt5.last_error()}")
                return False
        else:
            # Connect to already running MT5 terminal
            if not self.mt5.initialize():
                logger.error(f"MT5 initialize() failed, error code: {self.mt5.last_error()}")
                return False

        self.connected = True
        self.account_info = self.mt5.account_info()

        if self.account_info is None:
            logger.error("Failed to get account info")
            self.disconnect()
            return False

        logger.info(f"Connected to MT5 - Account: {self.account_info.login}")
        logger.info(f"Server: {self.account_info.server}, Balance: {self.account_info.balance}")

        return True

    def disconnect(self):
        """Disconnect from MT5 terminal"""
        if self.connected:
            self.mt5.shutdown()
            self.connected = False
            logger.info("Disconnected from MT5")

    def get_account_state(self) -> Optional[Dict]:
        """
        Get current account state

        Returns:
            Dictionary with account information or None if failed
        """
        if not self.connected:
            logger.error("Not connected to MT5")
            return None

        account = self.mt5.account_info()
        if account is None:
            logger.error("Failed to get account info")
            return None

        return {
            'balance': account.balance,
            'equity': account.equity,
            'margin': account.margin,
            'free_margin': account.margin_free,
            'profit': account.profit,
            'leverage': account.leverage,
            'login': account.login,
            'server': account.server,
            'currency': account.currency
        }

    def get_open_positions(self) -> List[Dict]:
        """
        Get all open positions (optionally filtered by magic number)

        Returns:
            List of position dictionaries
        """
        if not self.connected:
            logger.error("Not connected to MT5")
            return []

        positions = self.mt5.positions_get()

        if positions is None:
            logger.warning("No positions found or error getting positions")
            return []

        position_list = []
        for pos in positions:
            # Filter by magic number if specified
            if self.magic_filter is not None and pos.magic != self.magic_filter:
                continue

            position_list.append({
                'ticket': pos.ticket,
                'symbol': pos.symbol,
                'type': 'BUY' if pos.type == self.mt5.ORDER_TYPE_BUY else 'SELL',
                'volume': pos.volume,
                'price_open': pos.price_open,
                'price_current': pos.price_current,
                'sl': pos.sl,
                'tp': pos.tp,
                'profit': pos.profit,
                'magic': pos.magic,
                'comment': pos.comment,
                'time': datetime.fromtimestamp(pos.time)
            })

        return position_list

    def get_closed_trades_today(self) -> List[Dict]:
        """
        Get trades closed today

        Returns:
            List of closed trade dictionaries
        """
        if not self.connected:
            logger.error("Not connected to MT5")
            return []

        # Get deals from today
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        deals = self.mt5.history_deals_get(today, datetime.now())

        if deals is None:
            return []

        closed_trades = []
        for deal in deals:
            # Filter by magic number if specified
            if self.magic_filter is not None and deal.magic != self.magic_filter:
                continue

            # Only count out deals (position closes)
            if deal.entry == self.mt5.DEAL_ENTRY_OUT:
                closed_trades.append({
                    'ticket': deal.ticket,
                    'order': deal.order,
                    'symbol': deal.symbol,
                    'type': deal.type,
                    'volume': deal.volume,
                    'price': deal.price,
                    'profit': deal.profit,
                    'commission': deal.commission,
                    'swap': deal.swap,
                    'magic': deal.magic,
                    'time': datetime.fromtimestamp(deal.time)
                })

        return closed_trades

    def get_total_open_lots(self) -> float:
        """
        Calculate total open lot size across all positions

        Returns:
            Total lot size
        """
        positions = self.get_open_positions()
        return sum(pos['volume'] for pos in positions)

    def close_all_positions(self) -> Tuple[int, int]:
        """
        Close all open positions (respecting magic filter if set)

        Returns:
            Tuple of (successful_closes, failed_closes)
        """
        if not self.connected:
            logger.error("Not connected to MT5")
            return 0, 0

        positions = self.get_open_positions()
        successful = 0
        failed = 0

        for pos in positions:
            # Prepare close request
            symbol = pos['symbol']
            ticket = pos['ticket']
            volume = pos['volume']

            # Determine close type (opposite of open type)
            if pos['type'] == 'BUY':
                order_type = self.mt5.ORDER_TYPE_SELL
                price = self.mt5.symbol_info_tick(symbol).bid
            else:
                order_type = self.mt5.ORDER_TYPE_BUY
                price = self.mt5.symbol_info_tick(symbol).ask

            request = {
                "action": self.mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "position": ticket,
                "price": price,
                "deviation": 20,
                "magic": pos['magic'],
                "comment": "Rule breach - auto close",
                "type_time": self.mt5.ORDER_TIME_GTC,
                "type_filling": self.mt5.ORDER_FILLING_IOC,
            }

            result = self.mt5.order_send(request)

            if result.retcode == self.mt5.TRADE_RETCODE_DONE:
                logger.info(f"Position {ticket} closed successfully")
                successful += 1
            else:
                logger.error(f"Failed to close position {ticket}, error: {result.retcode}")
                failed += 1

        return successful, failed

    def get_symbol_info(self, symbol: str) -> Optional[Dict]:
        """
        Get symbol information

        Args:
            symbol: Symbol name (e.g., 'EURUSD')

        Returns:
            Dictionary with symbol info or None
        """
        if not self.connected:
            return None

        info = self.mt5.symbol_info(symbol)
        if info is None:
            return None

        return {
            'symbol': info.name,
            'bid': info.bid,
            'ask': info.ask,
            'spread': info.spread,
            'digits': info.digits,
            'point': info.point,
            'volume_min': info.volume_min,
            'volume_max': info.volume_max,
            'volume_step': info.volume_step
        }

