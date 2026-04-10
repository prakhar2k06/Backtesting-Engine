from data.base_data_handler import DataHandler
from core.event_queue import EventQueue
from core.event import MarketEvent
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import pandas as pd
from datetime import datetime
import os

class AlpacaHistoricalDataHandler(DataHandler):

    def __init__(self, api_key, secret_key, event_queue: EventQueue, symbols: list[str], analytics_engine = None):
        self.client = StockHistoricalDataClient(api_key, secret_key)
        self.event_queue = event_queue
        self.symbols = symbols
        self.analytics_engine = analytics_engine
        self.current_index = 0
        self.market_data = pd.DataFrame()
        self.latest_prices = {}
        self.timestamps = None
        self.price_matrix = None
    
    def load_data(self, start, end, timeframe=TimeFrame.Minute) -> None:
        cache_dir = "cache"
        os.makedirs(cache_dir, exist_ok=True)

        symbols_str = "_".join(self.symbols)
        filename = f"{symbols_str}_{timeframe}_{start.date()}_{end.date()}.parquet"
        cache_path = os.path.join(cache_dir, filename)

        if os.path.exists(cache_path):
            self.market_data = pd.read_parquet(cache_path)
            self.timestamps = self.market_data.index.to_numpy()
            self.price_matrix = self.market_data.to_numpy()

            return

        request = StockBarsRequest(symbol_or_symbols=self.symbols, timeframe=timeframe, start=start, end=end)
        bars = self.client.get_stock_bars(request)

        df = bars.df
        if df.empty:
            raise ValueError("No data returned from Alpaca for given date range")
        
        df = df.reset_index()
        df = df.pivot(index="timestamp", columns="symbol", values="close")

        if df.empty:
            raise ValueError("Pivoted dataframe is empty — check symbols/date range")

        df = df.sort_index()

        self.market_data = df

        self.timestamps = self.market_data.index.to_numpy()
        self.price_matrix = self.market_data.to_numpy()

        self.market_data.to_parquet(cache_path)

    def stream_next(self) -> None:
        if not self.has_next():
            return

        row = self.price_matrix[self.current_index]
        timestamp = self.timestamps[self.current_index]

        for i, symbol in enumerate(self.symbols):
            price = row[i]

            if price != price:
                continue

            price = float(price)

            self.latest_prices[symbol] = price

            features = {}
            if self.analytics_engine is not None:
                features = self.analytics_engine.update(symbol, price)

            event = MarketEvent(symbol, price, timestamp, features)
            self.event_queue.push_event(event)

        self.current_index += 1

    def has_next(self) -> bool:
        return self.current_index < len(self.market_data)
    
    def get_latest_price(self, symbol: str) -> float:
        return self.latest_prices.get(symbol)

    def get_latest_timestamp(self):
        if self.current_index == 0:
            return self.timestamps[0]
        
        return self.timestamps[self.current_index - 1]

    # Only for debugging
    def get_price_history(self, symbol: str):
        return self.market_data[symbol].iloc[:self.current_index]


