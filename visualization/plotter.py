import matplotlib.pyplot as plt
import pandas as pd


class Plotter:

    def __init__(self, portfolio, data_handler=None):
        self.portfolio = portfolio
        self.data_handler = data_handler

    def plot_equity_curve(self):

        equity = self.portfolio.holdings_history["total"]

        plt.figure()
        plt.plot(equity)
        plt.title("Equity Curve")
        plt.xlabel("Time")
        plt.ylabel("Portfolio Value")
        plt.grid()
        plt.show()

    def plot_drawdown(self):

        equity = self.portfolio.holdings_history["total"]

        drawdown = equity / equity.cummax() - 1

        plt.figure()
        plt.plot(drawdown)
        plt.title("Drawdown")
        plt.xlabel("Time")
        plt.ylabel("Drawdown")
        plt.grid()
        plt.show()

    def plot_trades(self, symbol):

        if self.data_handler is None:
            print("No data handler provided for price plotting")
            return

        if not hasattr(self.data_handler, "market_data"):
            print("Data handler has no dataframe")
            return

        price = self.data_handler.market_data[symbol]

        trades = self.portfolio.get_trade_log()

        if trades.empty:
            print("No trades to plot")
            return

        trades_symbol = trades[trades["symbol"] == symbol]

        buys = trades_symbol[trades_symbol["direction"] == "BUY"]
        sells = trades_symbol[trades_symbol["direction"] == "SELL"]

        plt.figure()

        plt.plot(price, label="Price")

        plt.scatter(
            buys["timestamp"],
            buys["price"],
            marker="^",
            label="Buy"
        )

        plt.scatter(
            sells["timestamp"],
            sells["price"],
            marker="v",
            label="Sell"
        )

        plt.legend()
        plt.title(f"Trades on {symbol}")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.grid()

        plt.show()