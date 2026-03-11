import pandas as pd
import numpy as np

def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0, periods_per_year: int = 252) -> float | None:
    excess_returns = returns - risk_free_rate / periods_per_year

    mean = excess_returns.mean()
    std = excess_returns.std()

    if std == 0:
        return None

    return np.sqrt(periods_per_year) * mean / std

def max_drawdown(equity_curve: pd.Series) -> float:
    cumulative_max = equity_curve.cummax()
    drawdown = (equity_curve - cumulative_max) / cumulative_max

    return drawdown.min()

def volatility(returns: pd.Series, periods_per_year: int = 252) -> float:
    return returns.std() * np.sqrt(periods_per_year)

def sortino_ratio(returns: pd.Series, risk_free_rate: int = 0, periods_per_year: int = 253) -> float | None:
    downside = returns[returns < 0]
    std = downside.std()

    if std == 0:
        return None

    excess_return = returns.mean() - risk_free_rate / periods_per_year

    return np.sqrt(periods_per_year) * excess_return / std

