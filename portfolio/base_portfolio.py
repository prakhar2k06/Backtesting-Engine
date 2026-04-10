from collections import defaultdict
from core.event import OrderEvent, SignalEvent
from core.enums import Direction, SignalType, OrderType


class BasePortfolio:

    def __init__(self, event_queue, data_handler, symbols):

        self.event_queue = event_queue
        self.data_handler = data_handler
        self.symbols = symbols

        self.positions = defaultdict(int)

        self.initial_capital = 100000
        self.cash = self.initial_capital

        self.max_position = 500
        self.risk_fraction = 0.1

    def process_signal_event(self, event: SignalEvent):

        order = self.generate_order(event)

        if order:
            self.event_queue.push_event(order)

    def generate_order(self, signal: SignalEvent):

        symbol = signal.symbol
        signal_type = signal.signal_type
        price = self.data_handler.get_latest_price(symbol)

        if price is None:
            return None

        current_position = self.positions[symbol]

        portfolio_value = self.cash + getattr(self, "market_value", 0)
        target_value = portfolio_value * self.risk_fraction

        quantity = int(target_value / price)

        if quantity <= 0:
            return None

        quantity = min(quantity, self.max_position)

        if signal_type == SignalType.BUY:

            if current_position > 0:
                return None

            if current_position < 0:
                quantity = abs(current_position)

            direction = Direction.BUY

        elif signal_type == SignalType.SELL:

            if current_position < 0:
                return None

            if current_position > 0:
                quantity = abs(current_position)

            direction = Direction.SELL

        else:
            return None

        return OrderEvent(symbol, direction, quantity, OrderType.MARKET)