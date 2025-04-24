# judas_ibkr/rebalancer.py

import json
from datetime import datetime as dt

from judas_ibkr.safe_order import safe_execute
from utils.broker_adapter import fetch_ibkr_state
from judas_reflective_intelligence.rebalance_scheduler_ai import generate_target_weights

class Rebalancer:
    def __init__(
        self,
        watch_list: list[str],
        leverage: float,
        threshold: float,
        max_trade_fraction: float,
        min_price_points: int,
        ib,  # your IB connection instance
    ):
        self.watch_list          = watch_list
        self.leverage            = leverage
        self.threshold           = threshold
        self.max_trade_fraction  = max_trade_fraction
        self.min_price_points    = min_price_points
        self.ib                  = ib
        self.prices              = {s: None for s in watch_list}
        self.last_rebalance_time = dt.utcnow()

    def update_price(self, symbol: str, price: float):
        self.prices[symbol] = price

    def should_rebalance(self, now=None):
        now = now or dt.utcnow()
        # simple time-based gate; you could add more logic here
        elapsed = (now - self.last_rebalance_time).total_seconds()
        return elapsed >= self.min_price_points and all(self.prices.values())

    async def execute(self):
        # 1) fetch current state
        result = await fetch_ibkr_state(self.ib)
        if isinstance(result, tuple) and len(result) == 2:
            cash, positions = result
        else:
            cash = result
            positions = {}  # assume no positions, or fetch them via another helper

        # 2) compute portfolio value
        total_value = cash + sum(self.prices[s] * positions.get(s, 0) for s in self.watch_list)

        # 3) compute target weights (AI model)
        target_weights = generate_target_weights(self.prices, total_value, positions)
    
        # 4) diff and issue trades
        for sym, w in target_weights.items():
            desired_qty = int(w * total_value / self.prices[sym])  # placeholder for desired quantity calculation
            current_qty = positions.get(sym, 0)  # current quantity from positions
            delta = desired_qty - current_qty
            price_ref = self.prices[sym]

            # Place the order via safe_execute(ib, sym, delta_qty, ref_price, guessed)
            # guessed=False means “don’t guess a limit price” (i.e. use market)
            safe_execute(
                self.ib,      # IB client
                sym,          # ticker symbol
                delta,        # +→BUY, -→SELL size
                price_ref,    # last tick price (or None)
                False         # guessed flag
            )
        self.last_rebalance_time = dt.utcnow()

    async def stream_and_rebalance(self, ps):
        msg = await ps.get_message(ignore_subscribe_messages=True, timeout=1.0)
        if msg and msg['type'] == 'message':
            payload = json.loads(msg['data'])
            # DEBUG: show every tick we get from Redis
            print(f"[{dt.now()}] Tick → {payload['s']} @ {payload['p']}")
            self.update_price(payload['s'], payload['p'])
        if self.should_rebalance(now=dt.utcnow()):
            print(f"[{dt.now()}] → Rebalance triggered")
            await self.execute()
