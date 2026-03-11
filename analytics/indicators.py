import pandas as pd

def sma(series: pd.Series, window: int) -> float | None:
    return series.rolling(window).mean().iloc[-1]

def ema(series: pd.Series, window: int) -> float | None:
    return series.ewm(span=window).mean().iloc[-1]
    
def momentum(series: pd.Series, window: int) -> float | None:
    if len(series) < window:
        return None
    return series.iloc[-1] - series.iloc[-window]

def rsi(series, window: int) -> float | None:
    if len(series) < window + 1:
        return None
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi.iloc[-1]

def macd(series: pd.Series) -> float | None:
    ema_short = series.ewm(span=12).mean()
    ema_long = series.ewm(span=26).mean()

    macd_line = ema_short - ema_long

    return macd_line.iloc[-1]
