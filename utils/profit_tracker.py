# utils/profit_tracker.py

from typing import Dict

class ProfitTracker:
    def __init__(self):
        self.entry_prices: Dict[str, float] = {}
        self.current_prices: Dict[str, float] = {}

    def update_entry(self, symbol: str, price: float):
        """Record a fresh entry price (buy signal)"""
        self.entry_prices[symbol] = price
        print(f"[ProfitTracker] Entry price for {symbol} set at {price}")

    def update_price(self, symbol: str, price: float):
        """Update live market price"""
        self.current_prices[symbol] = price

    def gain_percent(self, symbol: str) -> float:
        """Calculate % gain/loss"""
        entry = self.entry_prices.get(symbol)
        current = self.current_prices.get(symbol)
        if entry and current:
            return (current - entry) / entry * 100
        return 0.0

    def needs_take_profit(self, symbol: str, target_pct: float = 7.0) -> bool:
        """Check if gain exceeds the sacred profit target"""
        gain = self.gain_percent(symbol)
        if gain >= target_pct:
            print(f"[ProfitTracker] {symbol} reached +{gain:.2f}% gain — TAKE PROFIT recommended!")
            return True
        return False
