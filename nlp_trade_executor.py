# nlp_trade_executor.py

from trade_logger import TradeLogger
from shadow_account import ShadowAccount
from sizing_engine import calculate_position_size
from datetime import datetime

class NLPTradeExecutor:
    def __init__(self, trade_logger: TradeLogger, config=None, shadow_account=None):
        self.logger = trade_logger
        self.read_only = True
        self.shadow = shadow_account or ShadowAccount()
        self.config = config or {}

    def execute_trade(self, symbol, confidence_score, volatility, sentiment_index, side="BUY", reason=""):
        timestamp = datetime.utcnow().isoformat()
        equity = self.shadow.get_equity({})  # if price data available, pass here
        drawdown_pct = self.config.get("drawdown_pct", 0.0)
        base_pct = self.config.get("base_pct", 0.02)

        # Dynamic position size
        qty = calculate_position_size(
            equity=equity,
            sentiment_index=sentiment_index,
            confidence_score=confidence_score,
            volatility=volatility,
            drawdown_pct=drawdown_pct,
            base_pct=base_pct
        )

        price = 0.0  # Placeholder; replace with real-time feed if available

        self.logger.log_trade(
            symbol=symbol,
            side=side,
            qty=qty,
            price=price,
            reason=reason,
            timestamp=timestamp
        )

        self.shadow.execute_trade(
            symbol=symbol,
            side=side,
            qty=qty,
            price=price,
            reason=reason
        )

        print(f"🧾 NLP Trade: {side} {qty} {symbol} — {reason}")