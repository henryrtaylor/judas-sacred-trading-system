# -------------- multi_market_scheduler_polygon.py --------------
"""Stub scheduler using provider‑agnostic data_router.
Fetches a two‑day slice for each symbol in WATCH so we avoid
same‑day 403 on free tiers.
"""
from __future__ import annotations
import argparse, logging, datetime as _dt, sys
from pathlib import Path

# ------------------------------------------------------------------
# Ensure project root and utils package are on sys.path
# ------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))            # project root
sys.path.insert(0, str(ROOT / "utils"))  # utils directly

from utils.data_router import get_bars  # type: ignore

WATCH = ["SPY", "QQQ", "TLT", "GLD", "BTC-USD", "ETH-USD"]


def fetch_window(sym: str, date: str):
    start = _dt.date.fromisoformat(date)
    end   = (start + _dt.timedelta(days=1)).isoformat()
    return get_bars(sym, start=start.isoformat(), end=end)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--log-level", default="INFO")
    args = p.parse_args()

    logging.basicConfig(level=args.log_level.upper(), format="[SCHEDULER] %(message)s")
    for sym in WATCH:
        data = fetch_window(sym, args.date)
        if data and data.get("results"):
            logging.info("Fetched %s OK (%d bars)", sym, len(data["results"]))
        else:
            logging.warning("No data for %s", sym)
    logging.info("Scheduler finished dry‑run")


if __name__ == "__main__":
    main()