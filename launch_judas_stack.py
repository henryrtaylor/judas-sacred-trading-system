import subprocess
import time
import os
import webbrowser
from pathlib import Path

processes = []

WELCOME = """
=======================================
🧠 Welcome to the Judas Sacred System 🌌
=======================================
🌐 FastAPI API     → http://localhost:8000
🎨 React Dashboard → http://localhost:3000
📡 Socket Server   → Ready
🚀 Signal Emitter  → Listening...
🔒 Stay in flow, align with precision.
"""

def run_socket_server():
    print("📡 Starting Judas Socket Server...")
    processes.append(subprocess.Popen(["python", "judas_socket_server.py"]))

def run_fastapi_server():
    print("🌐 Starting FastAPI API...")
    processes.append(subprocess.Popen(["uvicorn", "api.main:app", "--reload"]))

def run_signal_emitter():
    print("🚀 Starting Signal Emitter...")
    processes.append(subprocess.Popen(["python", "signal_emitter.py"]))

def run_react_dashboard():
    print("🎨 Launching React Dashboard...")
    frontend_path = Path(__file__).parent / "frontend"
    if (frontend_path / "package.json").exists():
        try:
            subprocess.Popen(["npm", "run", "dev"], cwd=str(frontend_path))
            time.sleep(2)
            webbrowser.open("http://localhost:3000")
        except Exception as e:
            print(f"❌ Failed to launch React: {e}")
    else:
        print("⚠️ Frontend not found or package.json missing.")

def main():
    os.chdir(Path(__file__).parent)
    print(WELCOME)
    try:
        run_socket_server()
        time.sleep(1)
        run_fastapi_server()
        time.sleep(1)
        run_signal_emitter()
        time.sleep(1)
        run_react_dashboard()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping all processes...")
        for p in processes:
            p.terminate()

if __name__ == "__main__":
    main()
