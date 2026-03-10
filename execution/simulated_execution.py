from execution.execution_handler import ExecutionHandler
from core.event_queue import EventQueue
from data.data_handler import DataHandler
from core.event import OrderEvent, FillEvent
from datetime import datetime, timezone

class ExecutionSimulator(ExecutionHandler):
    def __init__(self,event_queue: EventQueue, data_handler: DataHandler):
        super().__init__(event_queue, data_handler)

    def process_order(self, order: OrderEvent) -> None:
        symbol = order.symbol
        direction = order.direction
        quantity = order.quantity

        event = FillEvent(symbol, direction, quantity, self.data_handler.get_latest_price(symbol), 0, datetime.now(timezone.utc))
        self.event_queue.push_event(event)

    
