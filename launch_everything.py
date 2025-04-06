import subprocess
import time
import os
import sys
from pathlib import Path

processes = []

def run_process(label, command, cwd=None):
    print(f"{label}...")
    try:
        proc = subprocess.Popen(command, cwd=cwd)
        processes.append(proc)
    except Exception as e:
        print(f"❌ Failed to start {label}: {e}")

def main():
    os.chdir(Path(__file__).parent)

    run_process("📡 Starting Judas Socket Server", [sys.executable, "judas_socket_server.py"])
    time.sleep(1)

    run_process("🌐 Starting FastAPI API", ["uvicorn", "api.main:app", "--reload"])
    time.sleep(1)

    run_process("🚀 Starting Signal Emitter", [sys.executable, "signal_emitter.py"])

    try:
        print("🎯 Judas System Live. Press CTRL+C to shut down.\n")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping all processes...")
        for p in processes:
            p.terminate()

if __name__ == "__main__":
    main()
