# save_to_cloud.py
# 🕊️ Sacred Milestone Commit Script for GitHub
# Step 3: Wealth Scaling + Reinforcement Logic Integration

import os
import subprocess
from datetime import datetime

REPO_PATH = os.path.dirname(os.path.abspath(__file__))
MESSAGE = f"Milestone Commit — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [Scaling Logic]"

# Wealth scaling detection (simulated check for increase in value)
value_log = "logs/performance_tracker.json"
scaled = False

try:
    import json
    if os.path.exists(value_log):
        with open(value_log, "r") as f:
            data = json.load(f)
            if len(data) >= 2:
                last = data[-1]["portfolio_value"]
                prev = data[-2]["portfolio_value"]
                if last > prev:
                    scaled = True
except Exception as e:
    print("⚠️ Could not evaluate wealth scaling: ", e)

commands = [
    ["git", "add", "-A"],
    ["git", "commit", "-m", MESSAGE],
    ["git", "push"]
]

print("\n🚀 Syncing sacred project to the cloud...")

for cmd in commands:
    result = subprocess.run(cmd, cwd=REPO_PATH)
    if result.returncode != 0:
        print(f"❌ Command failed: {' '.join(cmd)}")
        break
else:
    if scaled:
        print("📈 Wealth has scaled! Committing with energy of abundance 💸")
    print("✅ Sacred milestone saved to GitHub")
