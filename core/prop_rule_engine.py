"""
Prop Firm Rule Engine - Monitors and enforces prop firm rules
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class RuleViolation(Enum):
    """Types of rule violations"""
    MAX_DAILY_LOSS = "Max Daily Loss Exceeded"
    MAX_TOTAL_DRAWDOWN = "Max Total Drawdown Exceeded"
    LOT_SIZE_LIMIT = "Lot Size Limit Exceeded"
    CHALLENGE_EXPIRED = "Challenge Time Limit Exceeded"


class PropRuleEngine:
    """Monitors trading activity and enforces prop firm rules"""

    def __init__(self, firm_profile: Dict, starting_balance: float):
        """
        Initialize rule engine with firm profile

        Args:
            firm_profile: Dictionary containing firm rules
            starting_balance: Account starting balance
        """
        self.firm_profile = firm_profile
        self.starting_balance = starting_balance

        # Rule parameters
        self.max_daily_loss_percent = firm_profile.get('max_daily_loss_percent', 5.0)
        self.max_total_drawdown_percent = firm_profile.get('max_total_drawdown_percent', 10.0)
        self.profit_target_percent = firm_profile.get('profit_target_percent', 10.0)
        self.min_trading_days = firm_profile.get('min_trading_days', 5)
        self.challenge_days_limit = firm_profile.get('challenge_days_limit', 30)
        self.max_lot_per_trade = firm_profile.get('max_lot_per_trade', None)
        self.max_total_lots = firm_profile.get('max_total_lots', None)
        self.drawdown_type = firm_profile.get('drawdown_type', 'static')  # 'static' or 'trailing'

        # Calculate limits
        self.max_daily_loss = starting_balance * (self.max_daily_loss_percent / 100)
        self.max_total_drawdown = starting_balance * (self.max_total_drawdown_percent / 100)
        self.profit_target = starting_balance * (self.profit_target_percent / 100)

        # State tracking
        self.start_date = datetime.now()
        self.daily_starting_balance = starting_balance
        self.peak_balance = starting_balance
        self.trading_days: Set[str] = set()
        self.challenge_passed = False
        self.challenge_failed = False
        self.violation_reason = None

        logger.info(f"Rule Engine Initialized - {firm_profile['name']}")
        logger.info(f"Starting Balance: ${starting_balance:.2f}")
        logger.info(f"Max Daily Loss: ${self.max_daily_loss:.2f} ({self.max_daily_loss_percent}%)")
        logger.info(f"Max Total DD: ${self.max_total_drawdown:.2f} ({self.max_total_drawdown_percent}%)")
        logger.info(f"Profit Target: ${self.profit_target:.2f} ({self.profit_target_percent}%)")

    def check_new_day(self, current_balance: float) -> bool:
        """
        Check if it's a new trading day and reset daily tracking

        Args:
            current_balance: Current account balance

        Returns:
            True if new day detected
        """
        current_date = datetime.now().date()
        last_reset_date = getattr(self, 'last_reset_date', self.start_date.date())

        if current_date > last_reset_date:
            logger.info(f"New trading day detected: {current_date}")
            self.daily_starting_balance = current_balance
            self.last_reset_date = current_date
            return True

        return False

    def update_trading_days(self, closed_trades: List[Dict]):
        """
        Update set of days with closed trades

        Args:
            closed_trades: List of closed trades from today
        """
        if closed_trades:
            today = datetime.now().date().isoformat()
            if today not in self.trading_days:
                self.trading_days.add(today)
                logger.info(f"Trading day recorded: {today} (Total: {len(self.trading_days)} days)")

    def check_rules(self, account_state: Dict, open_positions: List[Dict],
                    closed_trades_today: List[Dict]) -> Optional[RuleViolation]:
        """
        Check all rules and return violation if any

        Args:
            account_state: Current account state from MT5
            open_positions: List of open positions
            closed_trades_today: List of trades closed today

        Returns:
            RuleViolation if violated, None otherwise
        """
        if self.challenge_failed:
            return None  # Already failed

        current_equity = account_state['equity']
        current_balance = account_state['balance']

        # Check for new day
        self.check_new_day(current_balance)

        # Update trading days
        self.update_trading_days(closed_trades_today)

        # Update peak for trailing drawdown
        if self.drawdown_type == 'trailing' and current_equity > self.peak_balance:
            self.peak_balance = current_equity
            logger.debug(f"New peak balance: ${self.peak_balance:.2f}")

        # 1. Check Daily Loss
        daily_loss = self.daily_starting_balance - current_equity
        if daily_loss > self.max_daily_loss:
            logger.error(f"DAILY LOSS BREACH: ${daily_loss:.2f} > ${self.max_daily_loss:.2f}")
            self.challenge_failed = True
            self.violation_reason = f"Daily loss ${daily_loss:.2f} exceeded limit ${self.max_daily_loss:.2f}"
            return RuleViolation.MAX_DAILY_LOSS

        # 2. Check Total Drawdown
        if self.drawdown_type == 'static':
            total_dd = self.starting_balance - current_equity
        else:  # trailing
            total_dd = self.peak_balance - current_equity

        if total_dd > self.max_total_drawdown:
            logger.error(f"TOTAL DRAWDOWN BREACH: ${total_dd:.2f} > ${self.max_total_drawdown:.2f}")
            self.challenge_failed = True
            self.violation_reason = f"Total drawdown ${total_dd:.2f} exceeded limit ${self.max_total_drawdown:.2f}"
            return RuleViolation.MAX_TOTAL_DRAWDOWN

        # 3. Check Lot Size Limits
        if self.max_lot_per_trade or self.max_total_lots:
            for pos in open_positions:
                if self.max_lot_per_trade and pos['volume'] > self.max_lot_per_trade:
                    logger.error(f"LOT SIZE BREACH: Position {pos['ticket']} has {pos['volume']} lots")
                    self.challenge_failed = True
                    self.violation_reason = f"Position lot size {pos['volume']} exceeded limit {self.max_lot_per_trade}"
                    return RuleViolation.LOT_SIZE_LIMIT

            if self.max_total_lots:
                total_lots = sum(pos['volume'] for pos in open_positions)
                if total_lots > self.max_total_lots:
                    logger.error(f"TOTAL LOTS BREACH: {total_lots} > {self.max_total_lots}")
                    self.challenge_failed = True
                    self.violation_reason = f"Total open lots {total_lots} exceeded limit {self.max_total_lots}"
                    return RuleViolation.LOT_SIZE_LIMIT

        # 4. Check Challenge Expiry
        days_elapsed = (datetime.now() - self.start_date).days
        if days_elapsed > self.challenge_days_limit:
            logger.error(f"CHALLENGE EXPIRED: {days_elapsed} days > {self.challenge_days_limit} days")
            self.challenge_failed = True
            self.violation_reason = f"Challenge expired after {days_elapsed} days"
            return RuleViolation.CHALLENGE_EXPIRED

        # 5. Check if target reached
        profit = current_balance - self.starting_balance
        if profit >= self.profit_target:
            if len(self.trading_days) >= self.min_trading_days:
                logger.info(f"🎉 CHALLENGE PASSED! Profit: ${profit:.2f}, Trading Days: {len(self.trading_days)}")
                self.challenge_passed = True
            else:
                logger.info(f"Target reached but need more trading days: {len(self.trading_days)}/{self.min_trading_days}")

        return None  # No violation

    def get_status_report(self, account_state: Dict) -> Dict:
        """
        Generate status report

        Args:
            account_state: Current account state

        Returns:
            Dictionary with status information
        """
        current_equity = account_state['equity']
        current_balance = account_state['balance']

        daily_loss = self.daily_starting_balance - current_equity
        daily_loss_percent = (daily_loss / self.starting_balance) * 100

        if self.drawdown_type == 'static':
            total_dd = self.starting_balance - current_equity
        else:
            total_dd = self.peak_balance - current_equity

        total_dd_percent = (total_dd / self.starting_balance) * 100

        profit = current_balance - self.starting_balance
        profit_percent = (profit / self.starting_balance) * 100

        days_elapsed = (datetime.now() - self.start_date).days

        return {
            'firm': self.firm_profile['name'],
            'status': 'PASSED' if self.challenge_passed else 'FAILED' if self.challenge_failed else 'ACTIVE',
            'current_balance': current_balance,
            'current_equity': current_equity,
            'starting_balance': self.starting_balance,
            'profit': profit,
            'profit_percent': profit_percent,
            'profit_target': self.profit_target,
            'daily_loss': daily_loss,
            'daily_loss_percent': daily_loss_percent,
            'daily_loss_limit': self.max_daily_loss,
            'total_drawdown': total_dd,
            'total_drawdown_percent': total_dd_percent,
            'total_drawdown_limit': self.max_total_drawdown,
            'trading_days': len(self.trading_days),
            'min_trading_days': self.min_trading_days,
            'days_elapsed': days_elapsed,
            'days_limit': self.challenge_days_limit,
            'violation_reason': self.violation_reason
        }

    def print_status(self, status: Dict):
        """Print formatted status report"""
        print("\n" + "="*70)
        print(f"  {status['firm']} - Challenge Status: {status['status']}")
        print("="*70)
        print(f"Balance: ${status['current_balance']:.2f} | Equity: ${status['current_equity']:.2f}")
        print(f"Profit: ${status['profit']:.2f} ({status['profit_percent']:.2f}%) / Target: ${status['profit_target']:.2f}")
        print("-"*70)
        print(f"Daily Loss: ${status['daily_loss']:.2f} ({status['daily_loss_percent']:.2f}%) / Limit: ${status['daily_loss_limit']:.2f}")
        print(f"Total DD: ${status['total_drawdown']:.2f} ({status['total_drawdown_percent']:.2f}%) / Limit: ${status['total_drawdown_limit']:.2f}")
        print("-"*70)
        print(f"Trading Days: {status['trading_days']}/{status['min_trading_days']} | Elapsed: {status['days_elapsed']}/{status['days_limit']} days")

        if status['violation_reason']:
            print(f"\n❌ VIOLATION: {status['violation_reason']}")

        print("="*70 + "\n")

