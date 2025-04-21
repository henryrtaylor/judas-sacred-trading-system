def verify_order(symbol, size, side, context="manual"):
    allowed_symbols = ["BTC-USD", "SPY", "GLD", "AAPL"]
    max_size = 100000  # Example USD limit

    if symbol not in allowed_symbols:
        raise ValueError(f"❌ Symbol {symbol} not allowed.")

    if abs(size) * 1000 > max_size:
        raise ValueError(f"❌ Size too large: {size} * 1000 > {max_size} USD notional.")

    print(f"✅ Order verified: {side} {symbol} size={size} ({context})")
    return True