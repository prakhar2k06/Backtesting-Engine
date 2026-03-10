from data.data_handler import DataHandler
from core.event_queue import EventQueue
from portfolio.portfolio_manager import Portfolio
from execution.execution_handler import ExecutionHandler
from strategy.base_strategy import Strategy
from core.event import MarketEvent, SignalEvent, OrderEvent, FillEvent

class TradingEngine:
    def __init__(self, data_handler: DataHandler, event_queue: EventQueue, strategy: Strategy, portfolio: Portfolio, execution_handler: ExecutionHandler):
        self.data_handler = data_handler
        self.event_queue = event_queue
        self.strategy = strategy
        self.portfolio = portfolio
        self.execution_handler = execution_handler

    def run(self) -> None:
        while self.data_handler.has_next():
            self.data_handler.stream_next()
            while not self.event_queue.is_empty():
                event = self.event_queue.pop_event()
                if isinstance(event, MarketEvent):
                    self.strategy.process_event(event)

                elif isinstance(event, SignalEvent):
                    self.portfolio.process_signal(event)

                elif isinstance(event, OrderEvent):
                    self.execution_handler.process_order(event)

                elif isinstance(event, FillEvent):
                    self.portfolio.process_fill(event)
            

