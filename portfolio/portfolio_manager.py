from data.data_handler import DataHandler
from core.event_queue import EventQueue
from core.event import SignalEvent, FillEvent, OrderEvent
from core.enums import Direction, SignalType, OrderType
from collections import defaultdict

class Portfolio:
    def __init__(self, event_queue: EventQueue, data_handler: DataHandler, symbols: list[str]):
        self.event_queue = event_queue
        self.data_handler = data_handler
        self.symbols = symbols
        self.positions = defaultdict(int)
        self.initial_capital = 100000
        self.cash = self.initial_capital
        self.holdings = defaultdict(int)
        self.portfolio_value = self.initial_capital
    
    def process_signal(self, event: SignalEvent) -> None:
        order = self.generate_order(event)

        if order is not None:
            self.event_queue.push_event(order)
    
    def process_fill(self, event: FillEvent) -> None:
        symbol = event.symbol
        direction = event.direction
        quantity = event.quantity
        fill_price = event.fill_price
        commission = event.commission
        
        if direction == Direction.BUY:
            self.positions[symbol] += quantity
            self.cash -= (quantity * fill_price) + commission

        elif direction == Direction.SELL:
            self.positions[symbol] -= quantity
            self.cash += (quantity * fill_price) - commission
        
        self.holdings[symbol] = self.positions[symbol] * self.data_handler.get_latest_price(symbol)
        self.portfolio_value = self.cash + sum(self.holdings.values())

    def generate_order(self, signal: SignalEvent) -> OrderEvent | None:
        symbol = signal.symbol
        signal_type = signal.signal_type
        timestamp = signal.timestamp

        quantity = 100

        if signal_type == SignalType.BUY:
            direction = Direction.BUY

        elif signal_type == SignalType.SELL:
            direction = Direction.SELL

        else:
            return None

        order = OrderEvent(symbol, direction, quantity, OrderType.MARKET)

        return order