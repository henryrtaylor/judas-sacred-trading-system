# ------------------ scripts/multi_market_scheduler.py -------
"""Example scheduler using new data_router."""
from __future__ import annotations
import argparse, logging, datetime as _dt, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "utils"))

from utils.data_router import get_bars

WATCH = ["SPY", "QQQ", "TLT", "GLD", "BTC-USD", "ETH-USD"]


def fetch_window(sym: str, day: str):
    d0 = _dt.date.fromisoformat(day)
    d1 = d0 + _dt.timedelta(days=1)
    return get_bars(sym, start=d0.isoformat(), end=d1.isoformat())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--log-level", default="INFO")
    args = p.parse_args()

    logging.basicConfig(level=args.log_level.upper(), format="[SCHEDULER] %(message)s")
    for sym in WATCH:
        js = fetch_window(sym, args.date)
        if js and js.get("results"):
            logging.info("Fetched %s OK (%d bars)", sym, len(js["results"]))
        else:
            logging.warning("No data for %s", sym)
    logging.info("Scheduler finished dry‑run")


if __name__ == "__main__":
    main()

