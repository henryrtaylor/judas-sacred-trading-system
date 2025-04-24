# modules/assets.py

def detect_market_type(symbol: str) -> str:
    symbol = symbol.upper()

    # Basic rules to guess market type
    if "/" in symbol:
        return "forex"
    elif symbol in {"BTC", "ETH", "DOGE", "SOL", "ADA"} or symbol.endswith("USD"):
        return "crypto"
    else:
        return "stock"
