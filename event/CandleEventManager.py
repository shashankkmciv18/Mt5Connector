from __future__ import annotations

from datetime import datetime
from typing import Callable
import logging

class CandleEventManager:

    def __init__(self, mt5):
        self.mt5 = mt5
        self._subscriptions: dict[str, list[Callable]] = {}  # "EURUSD_M5" -> [callbacks]
        self._last_candle_time: dict[str, datetime] = {}
        self._logger = logging.getLogger(__name__)

        self.TIMEFRAMES = {
            'M1':  mt5.TIMEFRAME_M1,
            'M5':  mt5.TIMEFRAME_M5,
            'M10': mt5.TIMEFRAME_M10,
            'M15': mt5.TIMEFRAME_M15,
        }

    def _key(self, symbol: str, timeframe: str) -> str:
        return f"{symbol.upper()}_{timeframe.upper()}"

    def subscribe(self, symbol: str, timeframe: str, callback: Callable):
        """
        Callback signature: fn(symbol: str, tf: str, candle_time: datetime) -> None
        """
        tf = timeframe.upper()
        sym = symbol.upper()

        if tf not in self.TIMEFRAMES:
            raise ValueError(f"Unknown timeframe '{tf}'. Valid: {list(self.TIMEFRAMES.keys())}")

        key = self._key(sym, tf)

        if key not in self._subscriptions:
            self._subscriptions[key] = []
            self._last_candle_time[key] = self._fetch_candle_time(sym, tf)  # seed
            self._logger.info(f"Subscribed to {sym} {tf} candle close")

        self._subscriptions[key].append(callback)

    def unsubscribe(self, symbol: str, timeframe: str, callback: Callable):
        key = self._key(symbol, timeframe)
        if key in self._subscriptions:
            self._subscriptions[key].remove(callback)

    def _fetch_candle_time(self, symbol: str, timeframe: str) -> datetime | None:
        rates = self.mt5.copy_rates_from_pos(symbol, self.TIMEFRAMES[timeframe], 0, 1)
        if rates is None or len(rates) == 0:
            return None
        return datetime.fromtimestamp(rates[0]['time'])

    def check(self):
        for key, callbacks in self._subscriptions.items():
            symbol, tf = key.rsplit('_', 1)
            current_time = self._fetch_candle_time(symbol, tf)
            if current_time is None:
                continue
            if current_time != self._last_candle_time.get(key):
                self._last_candle_time[key] = current_time
                self._logger.debug(f"[{symbol}][{tf}] Candle closed at {current_time}")
                for callback in callbacks:
                    try:
                        callback(symbol, tf, current_time)
                    except Exception as e:
                        self._logger.error(f"Error in {symbol} {tf} callback: {e}")