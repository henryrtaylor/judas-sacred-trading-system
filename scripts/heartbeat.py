# ---------- heartbeat.py ----------
"""Simple heartbeat: verifies that key log files have been updated within the
last N minutes; restarts services if stale.  Intended to be run hourly.
"""
import argparse, logging, os, subprocess, sys
from datetime import datetime, timedelta
from pathlib import Path

LOG_ROOT = Path("logs")
CHECKS = {
    "rebalance": LOG_ROOT / "rebalance_logs.log",
    "signal": LOG_ROOT / "signal_logs.log",
}


def main(threshold_min: int):
    logging.basicConfig(level=logging.INFO, format="[HEARTBEAT] %(message)s")
    stale = []
    for name, path in CHECKS.items():
        if not path.exists():
            stale.append(name)
            continue
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        if datetime.now() - mtime > timedelta(minutes=threshold_min):
            stale.append(name)
    if stale:
        logging.warning(f"Stale logs detected: {stale} → restarting …")
        for svc in stale:
            subprocess.run([sys.executable, "service_manager.py", "restart", svc])
    else:
        logging.info("All services healthy.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=int, default=60, help="Minutes before a log is considered stale")
    main(ap.parse_args().threshold)
