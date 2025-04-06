
# trade_executor.py
from datetime import datetime

class TradeExecutor:
    def __init__(self, broker_adapter, trade_logger=None, read_only=True, config=None):
        self.broker = broker_adapter
        self.logger = trade_logger
        self.read_only = read_only
        self.config = config or {}
        if 'live_mode' in self.config:
            self.read_only = not self.config['live_mode']

    def execute_trade(self, symbol, qty, side, reason):
        timestamp = datetime.utcnow().isoformat()

        # Pre-execution safety check
        if self.read_only:
            print(f"🔒 Read-only mode: {side} {qty} {symbol} NOT sent.")
            self._log(symbol, side, qty, price=None, reason=reason)
            return

        try:
            price = self.broker.place_order(symbol, qty, side)
            print(f"✅ Trade sent: {side} {qty} {symbol} @ {price}")
            self._log(symbol, side, qty, price, reason)
        except Exception as e:
            print(f"❌ Trade failed: {e}")
            self._log(symbol, side, qty, None, f"{reason} (ERROR: {e})")

    def _log(self, symbol, side, qty, price, reason):
        account_snapshot = self.broker.get_account_summary()
        if self.logger:
            self.logger.log_trade(
                symbol=symbol,
                side=side,
                qty=qty,
                price=price or 0.0,
                reason=reason,
                account_snapshot=account_snapshot
            )
