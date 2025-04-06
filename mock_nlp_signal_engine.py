
# mock_nlp_signal_engine.py

import random

BULLISH_KEYWORDS = ["record", "growth", "surge", "beats", "unveils", "expansion", "acquires"]
BEARISH_KEYWORDS = ["layoffs", "loss", "cut", "crash", "decline", "regulation", "probe", "delays", "warns", "recall"]

def interpret_headline(headline, openai_api_key=None, model=None):
    score = 0
    text = headline.lower()

    for word in BULLISH_KEYWORDS:
        if word in text:
            score += 1

    for word in BEARISH_KEYWORDS:
        if word in text:
            score -= 1

    if score > 0:
        signal = "BUY"
        confidence = min(0.6 + 0.1 * score, 0.95)
    elif score < 0:
        signal = "SELL"
        confidence = min(0.6 + 0.1 * abs(score), 0.95)
    else:
        signal = "IGNORE"
        confidence = 0.2

    return {
        "headline": headline,
        "symbol": extract_symbol(headline),
        "signal": signal,
        "reason": f"Keyword score: {score}",
        "confidence": round(confidence, 2)
    }

def extract_symbol(headline):
    known_symbols = ["AAPL", "TSLA", "NVDA", "MSFT", "BTC", "AMZN", "GOOGL"]
    for symbol in known_symbols:
        if symbol in headline.upper():
            return symbol
    return "UNKNOWN"
