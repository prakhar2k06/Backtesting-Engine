from analytics.risk_metrics import sharpe_ratio, max_drawdown, volatility, sortino_ratio
from portfolio.base_portfolio import BasePortfolio


class PerformanceTracker:
    def __init__(self, portfolio: BasePortfolio):
        self.portfolio = portfolio

    def compute_returns(self):
        equity = self.portfolio.holdings_history["total"]

        if equity.empty:
            return equity, equity

        returns = equity.pct_change(fill_method=None).dropna()
        return equity, returns

    def compute_metrics(self):
        equity, returns = self.compute_returns()

        if equity.empty:
            raise ValueError("Equity curve is empty — no data or no trades")

        metrics = {}
        metrics["Total Return"] = equity.iloc[-1] / equity.iloc[0] - 1
        metrics["Sharpe Ratio"] = sharpe_ratio(returns) if not returns.empty else None
        metrics["Sortino Ratio"] = sortino_ratio(returns) if not returns.empty else None
        metrics["Max Drawdown"] = max_drawdown(equity)
        metrics["Volatility"] = volatility(returns) if not returns.empty else None

        return metrics

    def report(self):
        metrics = self.compute_metrics()

        print("\nBacktest Performance")
        print("--------------------")

        for key, value in metrics.items():
            if isinstance(value, float):
                print(f"{key}: {value:.4f}")
            else:
                print(f"{key}: {value}")