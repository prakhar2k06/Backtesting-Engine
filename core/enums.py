from enum import Enum, auto

class SignalType(Enum):
    BUY = auto()
    SELL = auto()
    EXIT = auto()
    HOLD = auto()

class Direction(Enum):
    BUY = auto()
    SELL = auto()

class OrderType(Enum):
    MARKET = auto()
    LIMIT = auto()