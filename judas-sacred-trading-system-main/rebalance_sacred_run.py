import subprocess
import time
import sys

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--cash', type=float, default=1)
parser.add_argument('--dividends', type=float, default=0)
args = parser.parse_args()

sim_cmd = [
    "python", "rebalance_simulator.py",
    "--cash", str(args.cash),
    "--dividends", str(args.dividends)
]


# --- Parameters ---
sim_cmd = ["python", "rebalance_simulator.py", "--cash", "0", "--dividends", "0"]
exec_cmd = ["python", "rebalance_execute.py"]
pause_between = 2  # seconds
final_wait = 15    # seconds before auto-execute

print("🧠 Initiating Judas Protocol: 7x Sacred Rebalance Simulations...\n")

for i in range(7):
    print(f"🔁 Simulation {i+1}/7")
    subprocess.run(sim_cmd)
    time.sleep(pause_between)
    print("-" * 50)

# --- Auto-Execute Warning ---
print("\n✅ Simulations complete.")
print(f"⏳ You have {final_wait} seconds to cancel if you don't want to execute.")
print("🔌 Press CTRL+C now to abort.\n")

try:
    for sec in range(final_wait, 0, -1):
        sys.stdout.write(f"Executing in {sec} seconds...\r")
        sys.stdout.flush()
        time.sleep(1)
    print("\n🚀 Executing rebalance orders now...\n")
    subprocess.run(exec_cmd)

except KeyboardInterrupt:
    print("\n🛑 Execution canceled by user. Judas will wait until next time.")
