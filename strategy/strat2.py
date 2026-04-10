from strategy.base_strategy import Strategy
from core.event import MarketEvent, SignalEvent
from core.enums import SignalType
from core.logger import logger


class TrendMomentumStrategy(Strategy):

    def __init__(self, event_queue, data_handler, portfolio, symbols):
        super().__init__(event_queue, data_handler, portfolio, symbols)

        self.prev_fast = {}
        self.prev_slow = {}
        self.last_signal_time = {}

        # seconds
        self.cooldown = 20 * 120

    def process_event(self, event: MarketEvent):

        symbol = event.symbol

        fast_ma = event.features.get("sma_10")
        slow_ma = event.features.get("sma_50")

        if fast_ma is None or slow_ma is None:
            return

        prev_fast = self.prev_fast.get(symbol)
        prev_slow = self.prev_slow.get(symbol)

        self.prev_fast[symbol] = fast_ma
        self.prev_slow[symbol] = slow_ma

        if prev_fast is None or prev_slow is None:
            return

        last_time = self.last_signal_time.get(symbol)

        if last_time is not None:
            if (event.timestamp - last_time).total_seconds() < self.cooldown:
                return

        if prev_fast <= prev_slow and fast_ma > slow_ma:
            signal = SignalEvent(symbol, SignalType.BUY, event.timestamp)
            logger.info(f"STRATEGY BUY {symbol}")
            self.event_queue.push_event(signal)
            self.last_signal_time[symbol] = event.timestamp

        elif prev_fast >= prev_slow and fast_ma < slow_ma:
            signal = SignalEvent(symbol, SignalType.SELL, event.timestamp)
            logger.info(f"STRATEGY SELL {symbol}")
            self.event_queue.push_event(signal)
            self.last_signal_time[symbol] = event.timestamp