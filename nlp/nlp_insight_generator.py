
from datetime import datetime

def generate_commentary(signals):
    comments = []
    for sig in signals:
        if sig["signal"] == "BUY" and sig["confidence"] > 0.8:
            comments.append(f"{sig['symbol']} shows strong BUY confidence ({sig['confidence']:.2f}) at {sig['updated']}")
        elif sig["signal"] == "SELL":
            comments.append(f"Caution advised: {sig['symbol']} has SELL signal")
    return {
        "timestamp": datetime.now(),
        "insights": comments
    }
