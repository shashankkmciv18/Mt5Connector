from strategies.BaseStrategyInterface import BaseStrategy


class EMABreakoutStrategy(BaseStrategy):

    def __init__(self, mt5, candle_manager):
        super().__init__(mt5, candle_manager, name="EMABreakout")

    def subscribe_candles(self):
        self.candle_manager.subscribe('EURUSD', 'M5',  self.on_candle)
        self.candle_manager.subscribe('EURUSD', 'M15', self.on_candle)
        self.candle_manager.subscribe('GBPUSD', 'M5',  self.on_candle)

    def on_candle(self, symbol: str, tf: str, candle_time):
        if not self.is_active:
            return

        # Fetch the last N candles for your calculation
        rates = self.mt5.copy_rates_from_pos(symbol, self.candle_manager.TIMEFRAMES[tf], 0, 50)
        if rates is None:
            return

        # Your signal logic here
        close_prices = [r['close'] for r in rates]
        ema_fast = sum(close_prices[-9:])  / 9   # placeholder
        ema_slow = sum(close_prices[-21:]) / 21  # placeholder

        self.logger.info(f"[{symbol}][{tf}] EMA fast={ema_fast:.5f} slow={ema_slow:.5f}")

        if ema_fast > ema_slow:
            self._place_order(symbol, 'BUY')
        elif ema_fast < ema_slow:
            self._place_order(symbol, 'SELL')

    def _place_order(self, symbol: str, direction: str):
        self.logger.info(f"[{symbol}] Placing {direction} order...")

