import json
from pathlib import Path
from datetime import datetime

EVOLUTION_LOG = Path("logs/strategy_evolution.json")

def log_trade_result(symbol, strategy, confidence, result, zion_approved):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "strategy": strategy,
        "confidence": confidence,
        "result": result,
        "zion_approved": zion_approved
    }

    existing = []
    if EVOLUTION_LOG.exists():
        with open(EVOLUTION_LOG, "r") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []

    existing.append(log_entry)

    with open(EVOLUTION_LOG, "w") as f:
        json.dump(existing, f, indent=2)

    print(f"🧬 Evolution log saved: {symbol}, {result}, strategy={strategy}")

def summarize_strategy_performance():
    if not EVOLUTION_LOG.exists():
        print("No evolution data found.")
        return

    with open(EVOLUTION_LOG, "r") as f:
        data = json.load(f)

    summary = {}
    for entry in data:
        key = entry["strategy"]
        if key not in summary:
            summary[key] = {"count": 0, "wins": 0, "zion_passed": 0}

        summary[key]["count"] += 1
        if entry["result"] == "WIN":
            summary[key]["wins"] += 1
        if entry["zion_approved"]:
            summary[key]["zion_passed"] += 1

    print("📈 Strategy Evolution Summary:")
    for strategy, stats in summary.items():
        win_rate = round(stats["wins"] / stats["count"] * 100, 1)
        zion_rate = round(stats["zion_passed"] / stats["count"] * 100, 1)
        print(f"{strategy}: {stats['count']} trades | {win_rate}% win | {zion_rate}% Zion approved")

if __name__ == "__main__":
    summarize_strategy_performance()