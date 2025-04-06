"""
✴️ Judas Sacred Practice Runner ✴️
Harmonizing algorithmic intention with divine structure.
Aligned with sacred numbers, geometry, and cycles.
Version infused with symmetry, Fibonacci layering, and cycle-7 flow.
"""

import subprocess
import time
from datetime import datetime
import json
from pathlib import Path
import sys
import io

# 🔓 Force sacred UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 🌟 Sacred Constants
LOG_DIR         = Path("logs")
PERFORMANCE_LOG = LOG_DIR / "performance_tracker.json"
RUN_LOG         = LOG_DIR / "practice_run_log.txt"

LOG_DIR.mkdir(exist_ok=True)

# 🕊️ Invocation of Practice
print("\n🔺 Beginning Judas Daily Practice Run")
print("⏳ Timestamp:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# 🔻 Sacred Execution Flow
steps = [
   ("🧠 strategy", ["python", "judas_strategy_engine.py"]),
   ("🔮 simulate", ["python", "judas_simulate_rebalance.py"]),
   ("⚖️ execute", ["python", "rebalance_execute.py"]),
]

results = []
for label, cmd in steps:
    print(f"▶️ Initiating step: {label.center(24)}")
    try:
        result  = subprocess.run(cmd, capture_output=True, text=True, timeout=108)
        success = result.returncode == 0
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        output  = stdout + stderr

        results.append({
            "step":      label,
            "success":   success,
            "timestamp": datetime.now().isoformat(),
            "output":    output.strip()
        })

        print("📤 Output from", label)
        print("="*40)
        print(output.strip())
        print("="*40)

        symbol = "✅" if success else "❌"
        print(f"{symbol} {label.strip()} completed")

    except Exception as e:
        results.append({
            "step":      label,
            "success":   False,
            "timestamp": datetime.now().isoformat(),
            "output":    str(e)
        })
        print(f"❌ {label.strip()} exception: {e}")

# 🌕 Store to Sacred Chronicle
if PERFORMANCE_LOG.exists():
    with open(PERFORMANCE_LOG, 'r', encoding='utf-8') as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            history = []
else:
    history = []

summary = {
    "run_timestamp": datetime.now().isoformat(),
    "results": results
}
history.append(summary)

with open(PERFORMANCE_LOG, 'w', encoding='utf-8') as f:
    json.dump(history, f, indent=2)

# 📜 Scroll of Record
with open(RUN_LOG, 'a', encoding='utf-8') as f:
    f.write(f"\n[{datetime.now()}] Judas Practice Summary:\n")
    for r in results:
        f.write(f" - {r['step']}: {'✅' if r['success'] else '❌'}\n")

# 🧘 Completion Ritual
print("\n📦 Performance log updated:", PERFORMANCE_LOG)
print("📜 Session record stored at:", RUN_LOG)
print("🎴 Practice cycle complete — in harmony.")
