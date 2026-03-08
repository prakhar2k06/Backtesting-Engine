from datetime import datetime
from core.enums import SignalType, Direction, OrderType

class Event:
    pass

class MarketEvent(Event):
    def __init__(self, symbol: str, price: float, timestamp: datetime):
        self.type = "MARKET"
        self.symbol = symbol
        self.price = price
        self.timestamp = timestamp

class SignalEvent(Event):
    def __init__(self, symbol: str, signal_type: SignalType, timestamp: datetime):
        self.type = "SIGNAL"
        self.symbol = symbol
        self.signal_type = signal_type
        self.timestamp = timestamp

class OrderEvent(Event):
    def __init__(self, symbol: str, direction: Direction, quantity: int, order_type: OrderType):
        self.type = "ORDER"
        self.symbol = symbol
        self.direction = direction
        self.quantity = quantity
        self.order_type = order_type

class FillEvent(Event):
    def __init__(self, symbol: str, direction: Direction, quantity: int, fill_price: float, commission: float, timestamp: datetime):
        self.type = "FILL"
        self.symbol = symbol
        self.direction = direction
        self.quantity = quantity
        self.fill_price = fill_price
        self.commission = commission
        self.timestamp = timestamp

