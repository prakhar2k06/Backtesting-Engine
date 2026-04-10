from core.event_queue import EventQueue
from core.event import MarketEvent
from data.base_data_handler import DataHandler
import csv
from datetime import datetime
import pandas as pd

class CSVDataHandler(DataHandler):
    def __init__(self, event_queue: EventQueue, symbols: list[str]):
        self.event_queue = event_queue
        self.symbols = symbols
        self.current_index = 0
        self.market_data = pd.DataFrame()

    def load_data(self, path: str) -> None:
        df = pd.read_csv(path, parse_dates = ["timestamp"])
        df = df.pivot(index = "timestamp", columns = "symbol", values = "price")
        self.market_data = df

    def stream_next(self) -> None:
        if not self.has_next():
            return
        
        row = self.market_data.iloc[self.current_index]
        timestamp = self.market_data.index[self.current_index]
        
        for symbol in self.symbols:
            price = row[symbol]
            if pd.isna(price):
                continue
            event = MarketEvent(symbol, price, timestamp)
            self.event_queue.push_event(event)
        self.current_index += 1

    def has_next(self) -> bool:
        return self.current_index < len(self.market_data)
    
    def get_latest_price(self, symbol: str) -> float:
        return (self.market_data[symbol].iloc[:self.current_index].ffill().iloc[-1])

    def get_price_history(self, symbol: str):
        return self.market_data[symbol].iloc[:self.current_index]

    def get_latest_timestamp(self):
        if self.current_index == 0:
            return self.market_data.index[0]
        
        return self.market_data.index[self.current_index - 1]