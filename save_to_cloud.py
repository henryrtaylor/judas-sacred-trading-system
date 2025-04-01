# save_to_cloud.py
# 🕊️ Sacred Milestone Commit Script for GitHub

import os
import subprocess
from datetime import datetime

REPO_PATH = os.path.dirname(os.path.abspath(__file__))
MESSAGE = f"Milestone Commit — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

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
    print("✅ Sacred milestone saved to GitHub")
