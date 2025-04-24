"""
Guarded order placement: verifies a live quote before sending
a LIMIT order so Judas never overpays for a synthetic guess.
Requires ib_insync (pip install ib_insync) and an active TWS / IB Gateway.
"""

from __future__ import annotations
import logging, math
from ib_insync import IB, Stock, LimitOrder

_MAX_SLIP = 0.003     # 0.3 % max deviation allowed from guessed price

# ----------------------------------------------------------------------
def ibkr_market_price(ib: IB, sym: str) -> float:
    contract = Stock(sym, "SMART", "USD")
    ticker   = ib.reqMktData(contract, "", False, False)
    ib.sleep(0.4)                       # allow tick
    px = ticker.last or ticker.close or ticker.marketPrice()
    ib.cancelMktData(contract)
    if not px or math.isnan(px):
        raise RuntimeError(f"No live price for {sym}")
    return float(px)


def safe_execute(ib: IB,
                 sym: str,
                 delta_qty: float,
                 ref_price: float,
                 guessed: bool,
                 max_slip: float = _MAX_SLIP) -> None:
    """
    delta_qty : +shares to buy / ‑shares to sell
    ref_price : price used by the scheduler
    guessed   : True if ref_price was synthetic
    """
    side = "BUY" if delta_qty > 0 else "SELL"
    qty  = abs(int(delta_qty))
    if qty == 0:
        return

    try:
        live_px = ibkr_market_price(ib, sym)
    except Exception as e:
        logging.warning("quote fetch failed %s : %s", sym, e)
        return

    if guessed:
        slip = abs(live_px - ref_price) / ref_price
        if slip > max_slip:
            logging.info("ABORT %s slip %.2f%% > %.2f%%", sym, slip*100, max_slip*100)
            return

    limit_px = live_px * (1 + 0.001 * (1 if delta_qty > 0 else -1))
    contract = Stock(sym, "SMART", "USD")
    order    = LimitOrder(side, qty, round(limit_px, 2))
    ib.placeOrder(contract, order)
    logging.info("ORDER %s %d %s @ %.2f", side, qty, sym, limit_px)
