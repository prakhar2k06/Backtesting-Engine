from strategy.base_strategy import Strategy
from core.event_queue import EventQueue
from core.event import MarketEvent, SignalEvent
from data.data_handler import DataHandler
from core.enums import SignalType

class RandomStrat(Strategy):
    def __init__(self,event_queue: EventQueue, data_handler: DataHandler, symbols: list[str]):
        super().__init__(event_queue, data_handler, symbols)

    def process_event(self, event: MarketEvent) -> None:
        if event.symbol not in self.symbols:
            return
        
        if event.price < 100:
            new_event = SignalEvent(event.symbol, SignalType.BUY, event.timestamp)
        else: 
            new_event = SignalEvent(event.symbol, SignalType.SELL, event.timestamp)
        
        self.event_queue.push_event(new_event)

