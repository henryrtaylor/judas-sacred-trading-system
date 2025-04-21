import subprocess
import time
import sys
import os

def run_script(name, command):
    print(f"🔄 Starting: {name}")
    try:
        result = subprocess.run(command, check=True, shell=True)
        print(f"✅ {name} finished.\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ {name} failed: {e}")
        sys.exit(1)

def main():
    base_path = "C:/Users/Henry/Judas-IBKR_Project"

    os.chdir(base_path)
    print(f"🧠 Judas Warm-Up & Startup Sequence Initiated in: {base_path}\n")

    # Step 1: Warm-up sequence
    run_script("Quantum-Risk Matrix + Liquidity Oracle", "python judas-reflective-intelligence/judas_warm_up.py")

    # Step 2: Initialize Telegram bridge (assuming Phase 23)
    run_script("Telegram Command Listener", "python judas-reflective-intelligence/phase23_telegram/telegram_listener.py")

    # Optional future: Start paper rebalance loop
    # run_script("Rebalance Scheduler", "python judas-reflective-intelligence/rebalance_scheduler.py")

    print("🌟 All core functions loaded. Judas is ready to receive commands. 🕯️")

if __name__ == "__main__":
    main()