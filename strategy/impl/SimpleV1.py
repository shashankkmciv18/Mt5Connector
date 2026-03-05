from typing import Dict

from strategy.SimpleStrategy import Strategy
import random
from datetime import datetime, timedelta

class SimpleStrategy(Strategy):
    """Example strategy with random P&L"""

    def __init__(self, win_rate: float = 0.55, avg_win: float = 100, avg_loss: float = 80):
        self.win_rate = win_rate
        self.avg_win = avg_win
        self.avg_loss = avg_loss

    def generate_trade(self) -> Dict[str, float]:
        """Generate a single trade result"""
        is_win = random.random() < self.win_rate
        pnl = random.gauss(self.avg_win, 20) if is_win else -random.gauss(self.avg_loss, 15)
        return {'pnl': pnl, 'timestamp': datetime.now()}
