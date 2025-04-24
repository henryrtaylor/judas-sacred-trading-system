
# performance_logger.py
import json
import os
from datetime import datetime
from pathlib import Path

class PerformanceLogger:
    def __init__(self, log_path='logs/scheduler_performance.json'):
        self.log_path = log_path
        Path(os.path.dirname(log_path)).mkdir(parents=True, exist_ok=True)
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w') as f:
                json.dump([], f)

    def log_run(self, symbol, consensus, votes, num_trades):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": symbol,
            "consensus": consensus,
            "plugin_votes": votes,
            "num_trades": num_trades
        }
        with open(self.log_path, 'r+') as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
