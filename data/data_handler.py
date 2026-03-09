from core.event_queue import EventQueue
from core.event import MarketEvent
import csv
from datetime import datetime

class DataHandler:
    def __init__(self, event_queue: EventQueue, symbols: list[str]):
        self.event_queue = event_queue
        self.symbols = symbols
        self.dataset = []
        self.current_index = 0
        self.latest_prices = {}

    def load_data(self, path: str) -> None:
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbol = row["symbol"]
                if symbol not in self.symbols:
                    continue
                
                self.dataset.append({
                        "timestamp": datetime.fromisoformat(row["timestamp"]),
                        "symbol": symbol,
                        "price": float(row["price"]),
                    })
            self.dataset.sort(key=lambda x: x["timestamp"])

    def stream_next(self) -> None:
        if not self.has_next():
            return
        
        data = self.dataset[self.current_index]
        symbol = data["symbol"]
        price = data["price"]
        timestamp = data["timestamp"]

        self.latest_prices[symbol] = price
        event = MarketEvent(symbol, price, timestamp)
        self.event_queue.push_event(event)
        self.current_index += 1
    
    def has_next(self) -> bool:
        return self.current_index < len(self.dataset)
    
    def get_latest_price(self, symbol: str) -> float:
        return self.latest_prices[symbol]
