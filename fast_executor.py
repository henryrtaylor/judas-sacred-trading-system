# fast_executor.py

from shadow_account import ShadowAccount
from trade_logger import TradeLogger
from sizing_engine import calculate_position_size
from datetime import datetime

shadow = ShadowAccount()
logger = TradeLogger()

def execute_fast_trade(symbol, signal):
    equity = shadow.get_equity({})
    drawdown_pct = 0.0  # Optional add-in
    sentiment_index = 0.1  # Placeholder

    size = calculate_position_size(
        equity=equity,
        sentiment_index=sentiment_index,
        confidence_score=signal['confidence'],
        volatility=signal['volatility'],
        drawdown_pct=drawdown_pct
    )

    price = 0.0  # Replace with live feed if needed
    timestamp = datetime.utcnow().isoformat()

    logger.log_trade(
        symbol=symbol,
        side=signal['side'],
        qty=size,
        price=price,
        reason=signal['reason'],
        timestamp=timestamp
    )

    shadow.execute_trade(
        symbol=symbol,
        side=signal['side'],
        qty=size,
        price=price,
        reason=signal['reason']
    )

    print(f"⚡ Executed HFT Trade: {signal['side']} {size} {symbol} — {signal['reason']}")