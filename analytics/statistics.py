import pandas as pd

def rolling_mean(series: pd.Series, window: int) -> float | None:
    if len(series) < window:
        return None
    return series.rolling(window).mean().iloc[-1]

def rolling_std(series: pd.Series, window: int) -> float | None:
    if len(series) < window:
        return None
    return series.rolling(window).std().iloc[-1]

def z_score(series: pd.Series, window: int) -> float | None:
    if len(series) < window:
        return None
    
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()

    z = (series - mean) / std

    return z.iloc[-1]

def correlation(series1: pd.Series, series2: pd.Series, window: int) -> float | None:
    if len(series1) < window or len(series2) < window:
        return None
    
    return series1.rolling(window).corr(series2).iloc[-1]

def returns(series: pd.Series) -> pd.Series:
    return series.pct_change()

def volatility(series: pd.Series, window: int) -> float | None:
    if len(series) < window:
        return None

    r = series.pct_change()

    return r.rolling(window).std().iloc[-1]

