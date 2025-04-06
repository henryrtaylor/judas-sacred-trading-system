# fix_performance_log.py
# 🛠️ Clean + Enrich performance_tracker.json with missing portfolio values

import json
import os
from datetime import datetime
from pathlib import Path

PERF_LOG = "logs/performance_tracker.json"
DEFAULT_VALUE = 1000.0  # Start value if missing

Path("logs").mkdir(exist_ok=True)

if not os.path.exists(PERF_LOG):
    print("❌ performance_tracker.json not found.")
    exit()

with open(PERF_LOG, "r") as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError:
        print("❌ Invalid JSON in performance log.")
        exit()

for entry in data:
    if "timestamp" not in entry:
        entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if "portfolio_value" not in entry:
        entry["portfolio_value"] = DEFAULT_VALUE

# Save enriched log
with open(PERF_LOG, "w") as f:
    json.dump(data, f, indent=4)

print("✅ Enriched performance_tracker.json with defaults where needed.")
