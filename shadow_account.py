# shadow_account.py

from collections import defaultdict
from datetime import datetime

class ShadowAccount:
    def __init__(self, starting_cash=1_000_000):
        self.cash = starting_cash
        self.positions = defaultdict(lambda: {"qty": 0, "avg_price": 0.0})
        self.history = []

    def execute_trade(self, symbol, side, qty, price, reason):
        position = self.positions[symbol]
        total_cost = qty * price

        if side == "BUY":
            if self.cash >= total_cost:
                new_qty = position["qty"] + qty
                if new_qty == 0:
                    new_avg_price = 0
                else:
                    new_avg_price = (
                        (position["qty"] * position["avg_price"]) + total_cost
                    ) / new_qty
                position["qty"] = new_qty
                position["avg_price"] = new_avg_price
                self.cash -= total_cost
            else:
                print(f"💸 Not enough shadow cash to buy {qty} of {symbol}")
                return
        elif side == "SELL":
            if position["qty"] >= qty:
                position["qty"] -= qty
                self.cash += total_cost
            else:
                print(f"⚠️ Not enough shadow shares to sell {qty} of {symbol}")
                return

        self.positions[symbol] = position
        self.history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": price,
            "reason": reason
        })

    def get_equity(self, price_lookup: dict):
        equity = self.cash
        for symbol, position in self.positions.items():
            market_price = price_lookup.get(symbol, position["avg_price"])
            equity += position["qty"] * market_price
        return round(equity, 2)

    def print_summary(self, price_lookup=None):
        print("💼 Shadow Account Summary:")
        print(f"  Cash: ${self.cash:,.2f}")
        if price_lookup:
            equity = self.get_equity(price_lookup)
            print(f"  Total Equity: ${equity:,.2f}")
        print("  Positions:")
        for symbol, pos in self.positions.items():
            print(f"   - {symbol}: {pos['qty']} @ ${pos['avg_price']:.2f}")