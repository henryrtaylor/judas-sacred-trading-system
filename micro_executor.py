import sqlite3
from datetime import datetime

class MicroExecutor:
    def __init__(self, db_path='micro_trades.db'):
        self.db_path = db_path
        self._setup_db()

    def _setup_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS micro_trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    symbol TEXT,
                    side TEXT,
                    qty REAL,
                    price REAL,
                    confidence REAL,
                    volatility REAL,
                    reason TEXT
                )
            ''')
            conn.commit()

    def execute_trade(self, symbol, side, qty, price, confidence, volatility, reason=""):
        timestamp = datetime.utcnow().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO micro_trades (timestamp, symbol, side, qty, price, confidence, volatility, reason)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp, symbol, side, qty, price, confidence, volatility, reason))
            conn.commit()
        print(f"📉 Executed {side} {qty} {symbol} @ {price} | Confidence: {confidence}, Vol: {volatility}")