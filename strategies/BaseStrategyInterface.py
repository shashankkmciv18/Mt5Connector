import logging
from abc import ABC, abstractmethod

from event.CandleEventManager import CandleEventManager


class BaseStrategy(ABC):
    """
    All strategies inherit from this.
    Override on_candle() to implement your trade logic.
    """

    def __init__(self, mt5, candle_manager: CandleEventManager, name: str = "BaseStrategy"):
        self.mt5 = mt5
        self.candle_manager = candle_manager
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.is_active = False

    def start(self):
        """Subscribe to candles and activate strategy."""
        self.subscribe_candles()
        self.is_active = True
        self.logger.info(f"Strategy '{self.name}' started.")

    def stop(self):
        """Deactivate strategy."""
        self.is_active = False
        self.logger.info(f"Strategy '{self.name}' stopped.")

    @abstractmethod
    def subscribe_candles(self):
        """Define which symbols/timeframes to subscribe to."""
        pass

    @abstractmethod
    def on_candle(self, symbol: str, tf: str, candle_time):
        """Called on every subscribed candle close. Put trade logic here."""
        pass