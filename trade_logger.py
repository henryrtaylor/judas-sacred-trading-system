# trade_logger.py

import json
from datetime import datetime

class TradeLogger:
    def __init__(self, log_path='logs/trade_journal.json'):
        self.log_path = log_path

    def log_trade(self, symbol, side, qty, price, reason, timestamp=None):
        entry = {
            "timestamp": timestamp or datetime.utcnow().isoformat(),
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": price,
            "reason": reason
        }
        try:
            with open(self.log_path, 'a') as f:
                f.write(json.dumps(entry) + '\n')
            print(f"📜 Logged: {entry}")
        except Exception as e:
            print(f"⚠️ Failed to log trade: {e}")