# consensus_trade_router.py

from nlp_trade_executor import NLPTradeExecutor
from signal_engine import generate_signals
from trade_logger import TradeLogger
from shadow_account import ShadowAccount
from indicators import get_atr
from judas_config import CONFIG

import yfinance as yf

WATCHLIST = CONFIG.get("watchlist", ['AAPL', 'TSLA', 'NVDA', 'AMD'])

def final_vote_to_side(vote):
    if vote > 0:
        return "BUY"
    elif vote < 0:
        return "SELL"
    return None

def derived_from_vote(vote):
    return min(1.0, max(0.1, abs(vote) / 3))  # Normalize confidence score between 0.1–1.0

def calculate_sentiment_index():
    # Placeholder stub — in future, use real NLP & VIX-type measures
    return 0.1  # bullish slight sentiment

def atr_or_std(symbol):
    try:
        data = yf.download(symbol, period="14d", interval="1d", auto_adjust=True)
        return get_atr(data)[-1]
    except:
        return 1.0  # fallback

def run_consensus_router():
    shadow = ShadowAccount()
    logger = TradeLogger()
    executor = NLPTradeExecutor(trade_logger=logger, shadow_account=shadow)

    print("🧠 Routing consensus signals into NLP executor...")

    signals = generate_signals(WATCHLIST)

    for symbol, votes in signals.items():
        vote_value = sum(votes.values())
        side = final_vote_to_side(vote_value)
        if not side:
            print(f"🔍 {symbol} — NEUTRAL vote, skipping.")
            continue

        confidence_score = derived_from_vote(vote_value)
        volatility = atr_or_std(symbol)
        sentiment_index = calculate_sentiment_index()

        executor.execute_trade(
            symbol=symbol,
            confidence_score=confidence_score,
            volatility=volatility,
            sentiment_index=sentiment_index,
            side=side,
            reason="Consensus Signal"
        )