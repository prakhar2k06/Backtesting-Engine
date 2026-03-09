from core.event_queue import EventQueue
from core.event import MarketEvent, SignalEvent
from data.data_handler import DataHandler

class Strategy:
    def __init__(self, event_queue: EventQueue, data_handler: DataHandler, symbols: list[str]):
        self.event_queue = event_queue
        self.data_handler = data_handler
        self.symbols = symbols
    
    def process_event(self, event: MarketEvent) -> None:
        raise NotImplementedError


