# utils/trailing_stop_manager.py

from judas_ibkr.safe_order import safe_execute

class TrailingStopManager:
    """
    Tracks per-symbol peak prices and issues a sell when the price
    drops by drawdown_pct from that peak.
    """

    def __init__(self, ib, profit_tracker, drawdown_pct: float = 3.0):
        self.ib = ib
        self.profit_tracker = profit_tracker
        self.drawdown_pct = drawdown_pct
        self.peak_prices = {}

    def update_price(self, symbol: str, price: float):
        """
        On each tick, update the peak price if the new price is higher.
        """
        peak = self.peak_prices.get(symbol)
        if peak is None or price > peak:
            self.peak_prices[symbol] = price

    def check_and_execute(self, symbol: str, quantity: float):
        """
        If current price ≤ peak × (1 - drawdown_pct), sell `quantity`.
        """
        peak = self.peak_prices.get(symbol)
        if peak is None or quantity <= 0:
            return

        stop_price = peak * (1 - self.drawdown_pct / 100)
        current_price = self.profit_tracker.current_prices.get(symbol)
        if current_price is not None and current_price <= stop_price:
            print(f"[TrailingStop] {symbol} dropped to {current_price:.2f} <= stop {stop_price:.2f} → SELL {quantity}")
            safe_execute(self.ib, symbol, -quantity, None, False)
            # Reset peak to avoid immediate retrigger
            self.peak_prices[symbol] = current_price
