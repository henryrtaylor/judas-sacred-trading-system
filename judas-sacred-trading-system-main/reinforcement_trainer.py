# reinforcement_trainer.py
# 📈 Trains and saves reinforcement weights based on past performance

import json
import pandas as pd
from pathlib import Path
from sacred_logger import log_event

# === Load historical performance logs ===
log_file = Path("logs/performance_tracker.json")
if not log_file.exists():
    log_event("trainer", "❌ No performance log found.")
    exit()

performance_log = json.loads(log_file.read_text())

# === Extract returns by symbol ===
symbol_returns = {}
for entry in performance_log:
    portfolio = entry.get("allocations", {})
    perf = entry.get("portfolio_change", {})
    for sym, change in perf.items():
        if sym not in symbol_returns:
            symbol_returns[sym] = []
        symbol_returns[sym].append(change)

# === Calculate average return as reinforcement signal ===
weights = {}
for sym, returns in symbol_returns.items():
    avg_return = sum(returns) / len(returns) if returns else 0
    weights[sym] = round(avg_return, 4)

# === Normalize weights ===
total = sum(abs(v) for v in weights.values())
if total > 0:
    weights = {k: round(v / total, 4) for k, v in weights.items()}

# === Save sacred weights ===
Path("reinforcement").mkdir(exist_ok=True)
with open("reinforcement/reinforced_weights.json", "w") as f:
    json.dump(weights, f, indent=4)

log_event("trainer", f"✅ Reinforcement weights saved: {weights}")
print("🔁 Reinforcement learning weights updated.")
