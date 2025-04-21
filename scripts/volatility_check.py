# ---------- volatility_check.py ----------
"""Midday volatility hedge trigger.

If VIX > threshold OR SPX intraday drawdown exceeds threshold, the script
calls trade_executor.py with --reduce-risk 30 (default) to scale down positions.
"""
import argparse, logging, os, subprocess, sys
from datetime import datetime, time

THRESH_VIX = 22.0  # default
DRAW_THRESHOLD = 0.02  # 2 % intraday drop


def get_vix() -> float:
    # Placeholder: in production query Polygon or cached quote
    return 18.7


def intraday_spx_drawdown() -> float:
    # Placeholder stub
    return 0.005


def main(reduce_pct: int):
    logging.basicConfig(level=logging.INFO, format="[VOL‑CHECK] %(message)s")
    now = datetime.now().strftime("%H:%M:%S")
    logging.info(f"Checking noon volatility at {now} …")

    if get_vix() > THRESH_VIX or intraday_spx_drawdown() > DRAW_THRESHOLD:
        logging.warning("Volatility threshold breached → scaling down risk.")
        cmd = [sys.executable, "trade_executor.py", "--reduce-risk", str(reduce_pct)]
        subprocess.run(cmd, check=False)
    else:
        logging.info("Market calm → no action.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--reduce-pct", type=int, default=30)
    main(ap.parse_args().reduce_pct)
