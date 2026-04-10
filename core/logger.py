import logging
import os

# create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    filename="logs/trading_engine.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("trading_engine")