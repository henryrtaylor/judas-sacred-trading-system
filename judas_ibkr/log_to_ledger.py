import sqlite3
import json
from datetime import datetime

DB_PATH = "database/eternal_ledger.db"
MAX_RECORDS = 5000

def log_trade(symbol, signal, agent_votes, confidence_score, divine_law, sacred_flag=False, execution_notes=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO trades (timestamp, symbol, signal, agent_votes, confidence_score, divine_law, sacred_flag, execution_notes) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            timestamp, symbol, signal, json.dumps(agent_votes),
            confidence_score, divine_law, int(sacred_flag), execution_notes
        )
    )

    # Mobius memory cap enforcement
    cursor.execute("SELECT COUNT(*) FROM trades")
    count = cursor.fetchone()[0]
    if count > MAX_RECORDS:
        overflow = count - MAX_RECORDS
        cursor.execute("DELETE FROM trades WHERE id IN (SELECT id FROM trades ORDER BY id LIMIT ?)", (overflow,))

    conn.commit()
    conn.close()
    print(f"📜 Logged to Eternal Ledger: {symbol} → {signal} at {timestamp}")
