import time
import os
import subprocess
from datetime import datetime

def log_event(label):
    print(f"🕘 [{datetime.now().strftime('%H:%M:%S')}] {label}")

def run(name, cmd):
    log_event(f"Starting: {name}")
    try:
        subprocess.run(cmd, check=True, shell=True)
        log_event(f"✅ {name} completed.")
    except subprocess.CalledProcessError as e:
        log_event(f"❌ {name} failed: {e}")

def main():
    print("\n🧠 JUDAS DANGER ROOM SIMULATION INITIATED\n")

    # Morning Rebalance
    run("Morning Rebalance", "python judas-reflective-intelligence/rebalance_scheduler.py")

    # Midday: Simulated Market Volatility Spike
    time.sleep(2)
    log_event("⚠️ Simulating mid-day volatility spike... injecting abnormal liquidity drop...")
    run("Liquidity Oracle Refresh", "python judas-reflective-intelligence/phase15_cap_sym/collect_live.py")

    # Override Simulation Trigger
    time.sleep(1)
    log_event("⏳ Manually simulate override window (7s)... you may create 'override/stop.txt' now.")
    time.sleep(7)
    if os.path.exists("override/stop.txt"):
        log_event("⛔ OVERRIDE FILE DETECTED: Trade halted.")
        os.remove("override/stop.txt")
    else:
        run("Late Session Trade Execution", "python judas-reflective-intelligence/rebalance_scheduler.py")

    # Zion Council Reflection
    time.sleep(1)
    run("Zion Council Reflection", "python judas-reflective-intelligence/judgment_layer/zion_council.py")

    # End-of-Day Fire Reflection (Placeholder)
    log_event("🧾 Logging final reflections into inner_fire.py (simulated)")
    time.sleep(1)
    log_event("🕯️ Day complete. Judas has endured the fire. Danger Room shutdown.\n")

if __name__ == "__main__":
    main()