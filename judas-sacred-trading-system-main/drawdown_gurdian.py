# drawdown_guardian.py
# 🛡️ Drawdown Alert + Auto-De-Escalation System

import json
import os
from datetime import datetime
from pathlib import Path

PERF_LOG = "logs/performance_tracker.json"
GOALS_FILE = "generated/generated_goals.json"
MAX_DRAWDOWN = 0.10  # 10% drawdown
REDUCTION_FACTOR = 0.8  # reduce allocation weight

Path("logs").mkdir(exist_ok=True)
Path("generated").mkdir(exist_ok=True)

# Load performance log
def load_performance():
    if not os.path.exists(PERF_LOG):
        return []
    with open(PERF_LOG, "r") as f:
        return json.load(f)

# Load current allocation goals
def load_allocations():
    if not os.path.exists(GOALS_FILE):
        return {}
    with open(GOALS_FILE, "r") as f:
        return json.load(f)

# Detect drawdown and adjust goals
def check_drawdown(perf, alloc):
    if len(perf) < 2:
        print("⚠️ Not enough data to assess drawdown.")
        return alloc

    latest = perf[-1].get("portfolio_value")
    peak = max(p.get("portfolio_value", 0) for p in perf)

    if latest is None:
        print("❌ Latest portfolio value is missing.")
        return alloc

    drawdown = 1 - (latest / peak)
    print(f"📉 Detected Drawdown: {drawdown:.2%}")

    if drawdown >= MAX_DRAWDOWN:
        print("🚨 Max drawdown exceeded! Triggering auto-de-escalation...")
        reduced = {k: round(v * REDUCTION_FACTOR, 4) for k, v in alloc.items()}
        total = sum(reduced.values())
        normalized = {k: round(v / total, 4) for k, v in reduced.items()}
        return normalized

    print("✅ Within acceptable drawdown limits.")
    return alloc

# Save updated goals
def save_allocations(alloc):
    with open(GOALS_FILE, "w") as f:
        json.dump(alloc, f, indent=4)
    print("📤 Allocation goals updated with de-escalation logic.")

if __name__ == "__main__":
    perf = load_performance()
    alloc = load_allocations()
    adjusted = check_drawdown(perf, alloc)
    save_allocations(adjusted)
