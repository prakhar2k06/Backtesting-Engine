from core.event_queue import EventQueue
from data.data_handler import DataHandler
from core.event import OrderEvent

class ExecutionHandler:
    def __init__(self, event_queue: EventQueue, data_handler: DataHandler):
        self.event_queue = event_queue
        self.data_handler = data_handler
    
    def process_order(self, order: OrderEvent) -> None:
        raise NotImplementedError