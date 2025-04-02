# utils/logger.py

import logging
import csv
from datetime import datetime
from pathlib import Path

# Create logs directory if needed
Path("logs").mkdir(exist_ok=True)

# Set up main app logger
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def log_trade(contract, order, status):
    """Append trade info to CSV"""
    with open("logs/trades.csv", mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            contract.symbol,
            contract.secType,
            order.action,
            order.totalQuantity,
            getattr(status, 'avgFillPrice', 'N/A'),
            getattr(status, 'status', 'N/A')
        ])
