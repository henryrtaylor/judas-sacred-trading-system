import random

# Placeholder sentiment generator
def get_market_sentiment():
    sentiments = ["Bullish", "Bearish", "Neutral", "Fearful", "Greedy"]
    sentiment = random.choice(sentiments)
    print(f"🧠 Market Sentiment Detected: {sentiment}")
    return sentiment
