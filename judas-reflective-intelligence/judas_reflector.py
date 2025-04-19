import sqlite3
import json
from collections import defaultdict

def analyze_ledger(db_path="database/eternal_ledger.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT symbol, signal, agent_votes, divine_law, sacred_flag FROM trades ORDER BY id DESC LIMIT 1000")

    signals = defaultdict(int)
    sacred_trades = 0
    agent_stats = defaultdict(lambda: defaultdict(int))

    for symbol, signal, agent_votes, law, sacred in cursor.fetchall():
        signals[signal] += 1
        if sacred:
            sacred_trades += 1
        votes = json.loads(agent_votes)
        for agent, vote in votes.items():
            agent_stats[agent][vote] += 1

    print("\n🔍 Reflective Analysis:")
    print("Recent Signal Counts:", dict(signals))
    print(f"Sacred Trades: {sacred_trades}")
    print("\nAgent Voting Patterns:")
    for agent, votes in agent_stats.items():
        print(f"  {agent}: {dict(votes)}")

    conn.close()

if __name__ == "__main__":
    analyze_ledger()
