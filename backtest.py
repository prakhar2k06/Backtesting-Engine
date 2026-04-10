from core.event_queue import EventQueue
from data.csv_data_handler import CSVDataHandler
# from strategy.strat1 import MovingAverageCrossStrategy
from strategy.strat2 import TrendMomentumStrategy
from strategy.strat3 import TrendControlledStrategy
from strategy.strat4 import MeanReversionStrategy
from portfolio.backtest_portfolio import BacktestPortfolio
from execution.simulated_execution import ExecutionSimulator
from engine.trading_engine import TradingEngine
from performance.performance_tracker import PerformanceTracker
from data.alpaca_historical_data_handler import AlpacaHistoricalDataHandler
from analytics.trade_statistics import report
from analytics.engine import AnalyticsEngine
from datetime import datetime
from core.logger import logger
from visualization.plotter import Plotter

symbols = ["AAPL", "MSFT"]
event_queue = EventQueue()
analytics_engine = AnalyticsEngine(symbols)

data_handler = AlpacaHistoricalDataHandler(
    "PKDY3KWYDS2OKULPFYBSWUM5EO",
    "H92uJXwkb3x77tUJTGxP5SzSCE9m1YWt6ygWhB6gja6R",
    event_queue,
    symbols,
    analytics_engine
)

data_handler.load_data(
    start=datetime(2024,1,1),
    end=datetime(2025,1,1)
)
portfolio = BacktestPortfolio(event_queue, data_handler, symbols)
strategy = MeanReversionStrategy(event_queue, data_handler, portfolio, symbols)
execution = ExecutionSimulator(event_queue, data_handler)
tracker = PerformanceTracker(portfolio)
plotter = Plotter(portfolio, data_handler)
engine = TradingEngine("backtest", data_handler, event_queue, strategy, portfolio, execution)


print("DATA SHAPE:", data_handler.market_data.shape)
print(data_handler.market_data.head())
engine.run()
logger.info("Backtest finished")
print(portfolio.holdings_history)
tracker.report()
report(portfolio.get_trade_log())
plotter.plot_equity_curve()
plotter.plot_drawdown()
plotter.plot_trades("AAPL")

