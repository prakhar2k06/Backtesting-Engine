from analytics.indicators import RollingSMA, RollingEMA, RollingRSI, RollingMACD, RollingMomentum 

class AnalyticsEngine:
    def __init__(self, symbols: list[str]):
        self.sma_10 = {s: RollingSMA(10) for s in symbols}
        self.sma_20 = {s: RollingSMA(20) for s in symbols}
        self.sma_50 = {s: RollingSMA(50) for s in symbols}

        self.ema_10 = {s: RollingEMA(10) for s in symbols}
        self.momentum_10 = {s: RollingMomentum(10) for s in symbols}
        self.rsi_14 = {s: RollingRSI(14) for s in symbols}
        self.macd = {s: RollingMACD() for s in symbols}

    def update(self, symbol: str, price: float) -> dict:
        features = {}

        features["sma_10"] = self.sma_10[symbol].update(price)
        features["sma_20"] = self.sma_20[symbol].update(price)
        features["sma_50"] = self.sma_50[symbol].update(price)

        features["ema_10"] = self.ema_10[symbol].update(price)
        features["momentum_10"] = self.momentum_10[symbol].update(price)
        features["rsi_14"] = self.rsi_14[symbol].update(price)
        features["macd"] = self.macd[symbol].update(price)

        return features

     



