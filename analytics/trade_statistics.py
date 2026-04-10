import pandas as pd

def trade_pnl(trades: pd.DataFrame) -> pd.Series:
    if trades.empty:
        return pd.Series(dtype=float)

    pnl = []

    position = 0
    entry_price = None

    for _, row in trades.iterrows():
        direction = row["direction"]
        price = row["price"]
        qty = row["quantity"]

        if direction == "BUY":
            position += qty
            entry_price = price

        elif direction == "SELL":
            if entry_price is not None:
                pnl.append((price - entry_price) * qty)

            position -= qty

    return pd.Series(pnl)

def win_rate(pnl) -> float | None:
    if len(pnl) == 0:
        return None

    return (pnl > 0).mean()

def profit_factor(pnl) -> float | None:

    gains = pnl[pnl > 0].sum()
    losses = -pnl[pnl < 0].sum()

    if losses == 0:
        return None

    return gains / losses


def average_trade(pnl) -> float | None:

    if len(pnl) == 0:
        return None

    return pnl.mean()

def report(trades: pd.DataFrame) -> None:
    
    pnl = trade_pnl(trades)

    print("\nTrade Statistics")
    print("--------------------")
    print("Number of Trades:", len(pnl))
    print("Win Rate:", win_rate(pnl))
    print("Profit Factor:", profit_factor(pnl))
    print("Average Trade:", average_trade(pnl))