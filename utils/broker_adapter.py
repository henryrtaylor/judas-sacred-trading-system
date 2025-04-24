"""Thin wrapper for Interactive-Brokers API using ib_insync.
fetch_ibkr_state(ib: IB) ⟶ (cash_balance, positions_dict)
where positions_dict maps symbol → quantity. Assumes IB() is already connected.
"""
from __future__ import annotations
from typing import Dict, Tuple
from ib_insync import IB

async def fetch_ibkr_state(ib: IB) -> Tuple[float, Dict[str, float]]:
    """
    Given an already-connected IB instance, asynchronously fetch
    the account cash and positions as a dict of symbol to quantity.
    """
    # Async account summary
    summary = await ib.accountSummaryAsync()
    cash = 0.0
    for row in summary:
        if row.tag == "TotalCashValue" and row.currency == "USD":
            cash = float(row.value)
            break

    # Async positions using the proper async method
    positions_list = await ib.reqPositionsAsync()
    pos: Dict[str, float] = {}
    for p in positions_list:
        sym = p.contract.symbol
        # Append "-USD" for crypto positions
        if p.contract.secType == "CRYPTO":
            sym += "-USD"
        pos[sym] = float(p.position)

    return cash, pos
