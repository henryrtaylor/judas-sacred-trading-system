"""
backtest_week.py – condensed P/L printer
=======================================
Simulate Judas over the previous calendar week (Mon‑Fri).
Prints a **one‑line summary per day** with equity, cumulative P/L,
and how many prices were real vs guessed.  A final block shows the
week‑end balance.
"""
from __future__ import annotations
import logging, sys
from datetime import date, timedelta
from pathlib import Path
from typing import Dict
import redis.asyncio as aioredis
import asyncio
import os

# ── path bootstrap ───────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.extend([
    str(ROOT),
    str(ROOT / "utils"),
    str(ROOT / "judas_reflective_intelligence"),
])

# ── project imports ───────────────────────────────────────────
from utils.data_router import get_bars
from utils.broker_adapter import fetch_ibkr_state
from utils.guesser import guess_price, reward_guess
from judas_reflective_intelligence.rebalance_scheduler_ai import (
    generate_target_weights as calculate_target_weights,
)

WATCH = ["SPY", "QQQ", "TLT", "GLD", "BTC-USD", "ETH-USD"]

# ── redis tick helper ───────────────────────────────────────────
_RDS = aioredis.from_url(os.getenv("REDIS_URL", "redis://127.0.0.1:6379"))

async def _latest_tick(symbol: str) -> float | None:
    raw = await _RDS.get(f"tick:last:{symbol}")
    if not raw:
        return None
    try:
        return float(raw)
    except Exception:
        return None

# ── helpers ───────────────────────────────────────────────────

def last_week_dates() -> list[date]:
    today = date.today()
    last_mon = today - timedelta(days=today.weekday() + 7)
    return [last_mon + timedelta(days=i) for i in range(5)]

async def close_price(sym: str, day: date) -> float:
    if day == date.today():
        # fetch the latest tick asynchronously
        price = await _latest_tick(sym)
        if price is not None:
            return price

    nxt = day + timedelta(days=1)
    js = get_bars(sym, start=day.isoformat(), end=nxt.isoformat())
    if not js or not js.get("results"):
        raise ValueError(f"no bar {sym} {day}")
    rec = js["results"][0]
    return rec.get("c") or rec.get("Close") or next(iter(rec.values()))

async def main():
    # Async fetch of cash and positions
    cash, positions = await fetch_ibkr_state()

    logging.basicConfig(level=logging.INFO, format="[BT] %(message)s")
    logging.info("START cash %.2f  positions %s", cash, positions)

    start_equity: float | None = None

    for day in last_week_dates():
        symbols = sorted(set(WATCH).union(positions))

        prices: Dict[str, float] = {}
        guessed = 0
        for s in symbols:
            try:
                prices[s] = await close_price(s, day)
            except ValueError:
                px, _ = guess_price(s)
                prices[s] = px
                guessed += 1
        real = len(symbols) - guessed

        if real < 4:
            logging.warning("%s skipped (only %d real bars)", day, real)
            continue

        eq = cash + sum(positions.get(s, 0) * prices[s] for s in positions)
        if start_equity is None:
            start_equity = eq

        weights = calculate_target_weights(prices, eq, positions)
        target = {s: weights.get(s, 0) * eq / prices[s] for s in prices}

        for s, tgt in target.items():
            cur = positions.get(s, 0)
            delta = tgt - cur
            if abs(delta) < 1e-6:
                continue
            cash -= delta * prices[s]
            positions[s] = tgt

        eq = cash + sum(positions[s] * prices.get(s, 0) for s in positions)
        pnl = eq - start_equity
        logging.info(
            "%s  eq %.0f  P/L %.0f (%.2f%%)  real:%d  guess:%d",
            day, eq, pnl, pnl / start_equity * 100, real, guessed
        )

    if start_equity is None:
        logging.warning("No valid days – cannot compute P/L")
        sys.exit()

    # Final summary asynchronously
    final_prices = {s: await close_price(s, last_week_dates()[-1]) for s in positions}
    final_equity = cash + sum(positions[s] * final_prices[s] for s in positions)
    pnl = final_equity - start_equity
    logging.info("-------")
    logging.info("WEEK END equity %.2f", final_equity)
    logging.info("Total P/L  %.2f USD  (%.2f%%)", pnl, pnl / start_equity * 100)

if __name__ == "__main__":
    asyncio.run(main())
