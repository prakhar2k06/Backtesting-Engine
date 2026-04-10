from collections import deque

class RollingSMA:
    def __init__(self, window: int):
        self.window = window
        self.values = deque(maxlen = window)
        self.sum = 0.0
    
    def update(self, price: float):
        if len(self.values) == self.window:
            self.sum -= self.values[0]

        self.values.append(price)
        self.sum += price

        if len(self.values) < self.window:
            return None

        return self.sum / self.window
        
class RollingEMA:
    def __init__(self, window: int):
        self.alpha = 2 / (window + 1)
        self.ema = None
    
    def update(self, price: float):
        if self.ema is None:
            self.ema = price
        
        else:
            self.ema = self.alpha * price + (1 - self.alpha) * self.ema

        return self.ema
    
class RollingMomentum:
    def __init__(self, window: int):
        self.window = window
        self.values = deque(maxlen=window)

    def update(self, price: float):
        self.values.append(price)

        if len(self.values) < self.window:
            return None

        return price - self.values[0]

class RollingRSI:
    def __init__(self, window: int):
        self.window = window
        self.avg_gain = None
        self.avg_loss = None
        self.prev_price = None

    def update(self, price: float):
        if self.prev_price is None:
            self.prev_price = price
            return None

        delta = price - self.prev_price
        self.prev_price = price

        gain = max(delta, 0)
        loss = max(-delta, 0)

        if self.avg_gain is None:
            self.avg_gain = gain
            self.avg_loss = loss
        else:
            self.avg_gain = (self.avg_gain * (self.window - 1) + gain) / self.window
            self.avg_loss = (self.avg_loss * (self.window - 1) + loss) / self.window

        if self.avg_loss == 0:
            return 100

        rs = self.avg_gain / self.avg_loss
        return 100 - (100 / (1 + rs))

class RollingMACD:
    def __init__(self):
        self.ema_fast = RollingEMA(12)
        self.ema_slow = RollingEMA(26)
        self.signal = RollingEMA(9)

    def update(self, price: float):
        fast = self.ema_fast.update(price)
        slow = self.ema_slow.update(price)

        if fast is None or slow is None:
            return None

        macd = fast - slow
        signal = self.signal.update(macd)

        if signal is None:
            return None

        return macd - signal