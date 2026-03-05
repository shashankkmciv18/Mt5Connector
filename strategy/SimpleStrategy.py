from abc import ABC, abstractmethod
from typing import List, Dict



class Strategy(ABC):
    """Base class for trading strategies"""

    @abstractmethod
    def generate_trade(self) -> Dict[str, float]:
        """Generate a trade with profit/loss"""
        pass

