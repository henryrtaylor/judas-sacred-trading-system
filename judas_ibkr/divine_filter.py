import random
from insight.market_sentiment import get_market_sentiment
from insight.volatility_guard import check_volatility_conditions
from insight.time_windows import get_current_window


def load_guidelines(path="divine_guidelines.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            laws = [line.strip() for line in f.readlines() if line.strip()]
        return laws
    except FileNotFoundError:
        print("⚠️ divine_guidelines.txt not found.")
        return []

def reflect_before_trade(symbol, signal, sacred_symbol="ARKK"):
    laws = load_guidelines()
    if not laws:
        return

    chosen_law = random.choice(laws)
    print("\n🕊️ DIVINE FILTER ENGAGED")
    print(f"Guideline: “{chosen_law}”")

    if symbol == sacred_symbol:
        print(f"✨ Sacred Symbol '{symbol}' detected. Elevating confirmation layer...")
        print("🔔 ARKK is being handled with spiritual reverence.")

    print(f"→ Trade Intention: {signal} {symbol}\n")
    return chosen_law
