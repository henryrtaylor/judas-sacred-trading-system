import threading
import subprocess
import time
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("start_judas")

def find_virtual_env():
    """
    Dynamically locate the virtual environment's Python interpreter.
    """
    venv_path = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
    if os.path.exists(venv_path):
        return venv_path

    current_dir = os.getcwd()
    while current_dir != os.path.dirname(current_dir):
        venv_path = os.path.join(current_dir, ".venv", "Scripts", "python.exe")
        if os.path.exists(venv_path):
            return venv_path
        current_dir = os.path.dirname(current_dir)

    return None

def threaded_run_socket_server(python_path):
    logger.info("🚀 Launching Judas Socket Server...")
    subprocess.run([python_path, "judas_socket_server.py"])

def threaded_run_scheduler(python_path):
    logger.info("🕰️ Starting Scheduler Heartbeat...")
    subprocess.run([python_path, "scheduler_heartbeat.py"])

if __name__ == "__main__":
    python_path = find_virtual_env()
    if not python_path:
        logger.error("❌ Could not find virtual environment Python interpreter.")
        sys.exit(1)

    logger.info(f"✅ Using Python interpreter at: {python_path}")
    threading.Thread(target=threaded_run_socket_server, args=(python_path,), daemon=True).start()
    threading.Thread(target=threaded_run_scheduler, args=(python_path,), daemon=True).start()

    while True:
        time.sleep(10)
