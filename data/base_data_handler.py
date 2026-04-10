class DataHandler:
    def stream_next(self):
        raise NotImplementedError

    def get_latest_price(self, symbol):
        raise NotImplementedError

    def get_price_history(self, symbol):
        raise NotImplementedError