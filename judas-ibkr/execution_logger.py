import csv
from datetime import datetime
import os

def log_execution(symbol, size, side, price, context="manual", path="logs/execution_logs.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    row = [datetime.utcnow().isoformat(), symbol, size, side, price, context]
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)
    print(f"🧾 Execution logged: {row}")