# reinforcement_feedback.py
# 📈 Judas Reinforcement Feedback Engine — Adaptive Allocation Logic

import json
import os
from datetime import datetime
from pathlib import Path

PERF_LOG = "logs/performance_tracker.json"
GOALS_FILE = "generated/generated_goals.json"
SCALE_FACTOR = 1.1  # how much to boost scores on success

def load_performance():
    if os.path.exists(PERF_LOG):
        with open(PERF_LOG, "r") as f:
            return json.load(f)
    return []

def load_allocations():
    if os.path.exists(GOALS_FILE):
        with open(GOALS_FILE, "r") as f:
            return json.load(f)
    return {}

def reinforce_allocations(performance, allocations):
    if len(performance) < 2:
        print("⚠️ Not enough performance history to evaluate reinforcement.")
        return allocations

    last = performance[-1]
    prev = performance[-2]

    if "portfolio_value" not in last or "portfolio_value" not in prev:
        print("⚠️ Missing 'portfolio_value' in performance log.")
        return allocations

    updated = allocations.copy()

    if last["portfolio_value"] > prev["portfolio_value"]:
        print("✅ Reinforcement triggered: portfolio value increased.")
        for asset in updated:
            updated[asset] *= SCALE_FACTOR
    else:
        print("🔁 No change or drop in value — allocations unchanged.")

    # Normalize
    total = sum(updated.values())
    for k in updated:
        updated[k] = round(updated[k] / total, 4)

    return updated

def save_allocations(updated):
    Path("generated").mkdir(exist_ok=True)
    with open(GOALS_FILE, "w") as f:
        json.dump(updated, f, indent=4)
    print("📤 Updated strategy goals with reinforcement adjustments.")

if __name__ == "__main__":
    perf = load_performance()
    alloc = load_allocations()
    new_alloc = reinforce_allocations(perf, alloc)
    save_allocations(new_alloc)
