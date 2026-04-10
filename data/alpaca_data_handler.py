from data.base_data_handler import DataHandler
from core.event import MarketEvent
from alpaca.data.live import StockDataStream
from alpaca.data.enums import DataFeed
from datetime import datetime


class AlpacaDataHandler(DataHandler):

    def __init__(self, api_key, secret_key, event_queue, symbols):

        self.event_queue = event_queue
        self.symbols = symbols
        self.latest_prices = {}

        self.stream = StockDataStream(
            api_key,
            secret_key,
            feed=DataFeed.IEX
        )

    def subscribe(self):

        self.stream.subscribe_trades(self._on_trade, *self.symbols)

    async def _on_trade(self, trade):

        symbol = trade.symbol
        price = trade.price
        timestamp = trade.timestamp

        print("Trade:", symbol, price)

        self.latest_prices[symbol] = price

        event = MarketEvent(
            symbol,
            price,
            timestamp
        )

        self.event_queue.push_event(event)

    def start(self):

        self.subscribe()
        self.stream.run()

    def get_latest_price(self, symbol):

        return self.latest_prices.get(symbol)

    def get_price_history(self):

        return None