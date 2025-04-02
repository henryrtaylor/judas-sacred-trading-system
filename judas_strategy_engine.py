# judas_strategy_engine.py
# Sacred Multi-Asset Strategy Engine v2.0 ✨ (Now with AI Predictive Insight + Reinforcement Feedback)

import pandas as pd
import os
import json
from datetime import datetime
from pathlib import Path

# Sacred Import Hooks
from modules.utils import clean_price_data
from modules.assets import detect_market_type
from modules.scoring import score_strategy_stock, score_strategy_forex, score_strategy_crypto
from modules.ai_predictor import predict_stock_signal
from reinforcement_engine import apply_reinforced_weights
from sacred_logger import log_event

# Load data
price_file = "logs/historical_prices.csv"
try:
    df = pd.read_csv(price_file)
    df = clean_price_data(df)
except Exception as e:
    log_event("strategy", f"❌ Failed to load historical data: {e}")
    exit()

# Ensure we have valid symbols
symbols = df['symbol'].unique()
valid_symbols = []
allocations = {}


def get_strategy_score(symbol, df_symbol):
    market_type = detect_market_type(symbol)

    if market_type == "stock":
        ai_score = predict_stock_signal(df_symbol)
        if ai_score is not None:
            log_event("strategy", f"🧠 AI score for {symbol}: {ai_score}")
            return ai_score
        return score_strategy_stock(df_symbol)

    elif market_type == "forex":
        return score_strategy_forex(df_symbol)

    elif market_type == "crypto":
        return score_strategy_crypto(df_symbol)

    return None

# Evaluate each symbol
for symbol in symbols:
    df_symbol = df[df['symbol'] == symbol].copy()
    if df_symbol.shape[0] < 30:
        log_event("strategy", f"⚠️ Skipping {symbol}: not enough data")
        continue

    score = get_strategy_score(symbol, df_symbol)
    if score is not None:
        allocations[symbol] = score
        valid_symbols.append(symbol)
    else:
        log_event("strategy", f"⚠️ Skipping {symbol}: scoring failed")

# Normalize and sort
if not allocations:
    log_event("strategy", "❌ No valid allocations after scoring")
    exit()

total_score = sum(allocations.values())
raw_allocations = {k: round(v / total_score, 4) for k, v in allocations.items()}
raw_allocations = dict(sorted(raw_allocations.items(), key=lambda x: x[1], reverse=True))

# ✨ Apply reinforcement engine
reinforced_alloc = apply_reinforced_weights(raw_allocations, log_path="logs/performance_tracker.json")

# Save sacred allocation
Path("generated").mkdir(exist_ok=True)
with open("generated/generated_goals.json", "w") as f:
    json.dump(reinforced_alloc, f, indent=4)

log_event("strategy", f"✅ Multi-Asset Strategy complete. Allocated: {list(reinforced_alloc.keys())}")
