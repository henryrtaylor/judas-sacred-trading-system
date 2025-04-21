# -------------- practice_runner.py --------------
from __future__ import annotations
"""Dry‑run harness for Judas trading DAG.

Simulates a full trad...
    }
  ]
}

Simulates a full trading day (or the date passed via --date) by
invoking multi_market_scheduler_polygon.py in dry‑run mode.  It’s
meant for safe testing before live execution.
"""
import sys, subprocess, logging, argparse
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCRIPT_CANDIDATES = [
    ROOT / "multi_market_scheduler_polygon.py",
    ROOT / "judas-reflective-intelligence" / "multi_market_scheduler_polygon.py",
]

def locate_script() -> Path:
    for p in SCRIPT_CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError("multi_market_scheduler_polygon.py not found in expected locations")


def run(date: str, log_level: str):
    sched = locate_script()
    cmd = [sys.executable, str(sched), "--dry-run", "--date", date, "--log-level", log_level]
    logging.info("[PRACTICE] Launching %s", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default="tomorrow")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    if args.date.lower() == "tomorrow":
        tgt = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        tgt = args.date

    logging.basicConfig(level=args.log_level.upper(), format="%(message)s")
    logging.info("[PRACTICE] Simulating date %s …", tgt)
    run(tgt, args.log_level.upper())

if __name__ == "__main__":
    main()
