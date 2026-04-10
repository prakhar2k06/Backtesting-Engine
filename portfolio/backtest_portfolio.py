import pandas as pd
from core.event import FillEvent
from core.enums import Direction
from core.logger import logger
from portfolio.base_portfolio import BasePortfolio


class BacktestPortfolio(BasePortfolio):

    def __init__(self, event_queue, data_handler, symbols):
        super().__init__(event_queue, data_handler, symbols)

        self.market_value = 0.0
        self.portfolio_value = self.initial_capital

        self.holdings_history = pd.DataFrame(
            columns=["cash", "holdings", "total"]
        ).astype(float)

        self.trades = []

    def process_market_event(self, event):

        self.update_holdings(event.timestamp)

    def process_fill(self, event: FillEvent):

        symbol = event.symbol
        direction = event.direction
        quantity = event.quantity
        fill_price = event.fill_price
        commission = event.commission
        timestamp = event.timestamp

        if direction == Direction.BUY:
            self.positions[symbol] += quantity
            self.cash -= (quantity * fill_price) + commission

        elif direction == Direction.SELL:
            self.positions[symbol] -= quantity
            self.cash += (quantity * fill_price) - commission

        self.trades.append({
            "timestamp": timestamp,
            "symbol": symbol,
            "direction": direction.name,
            "quantity": quantity,
            "price": fill_price,
            "commission": commission
        })

        self.update_holdings(timestamp)

        logger.info(
            f"PORTFOLIO UPDATE {symbol} {direction.name} "
            f"qty={quantity} price={fill_price} cash={self.cash}"
        )

    def update_holdings(self, timestamp):

        if (
            not self.holdings_history.empty
            and self.holdings_history.index[-1] == timestamp
        ):
            return

        holdings_value = 0

        for symbol, qty in self.positions.items():
            price = self.data_handler.get_latest_price(symbol)

            if price is None or pd.isna(price):
                continue

            holdings_value += qty * price

        self.market_value = holdings_value
        total_value = self.cash + holdings_value
        self.portfolio_value = total_value

        row = pd.DataFrame({
            "cash": [self.cash],
            "holdings": [holdings_value],
            "total": [total_value]
        }, index=[timestamp])

        if self.holdings_history.empty:
            self.holdings_history = row
        else:
            self.holdings_history = pd.concat([self.holdings_history, row], ignore_index=False)

    def get_trade_log(self):
        return pd.DataFrame(self.trades)