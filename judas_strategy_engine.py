"""
✴️ Judas Strategy Engine ✴️
Infused with universal encoding. Empowering clarity.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pandas as pd
from datetime import datetime
from pathlib import Path
import json

# 🔺 Configurations
DATA_PATH = Path("logs/historical_prices.csv")
GOALS_PATH = Path("generated/generated_goals.json")
LOG_PATH = Path("logs/judas_diagnostics.log")
STRATEGY_LOG_PATH = Path("logs/judas_strategy_log.json")

# 📜 Sacred Constants
MIN_VALID_ROWS = 10
SYMBOL_COLUMN = "symbol"

# 🌌 Load Market Data
try:
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
except Exception as e:
    print(f"❌ Failed to load data: {e}")
    exit(1)

# 🌀 Initialize Structures
scores = []
clean_symbols = df[SYMBOL_COLUMN].unique()

# 🧠 Strategy Logic
for symbol in clean_symbols:
    df_symbol = df[df[SYMBOL_COLUMN] == symbol].copy()
    df_symbol = df_symbol.sort_values("date")

    if df_symbol["close"].count() < MIN_VALID_ROWS:
        print(f"⚠️ Skipping {symbol}: After cleaning, not enough valid price rows.")
        continue

    df_symbol["momentum"] = df_symbol["close"].pct_change(periods=3)
    df_symbol["slope"] = df_symbol["close"].rolling(5).mean().diff()
    score = df_symbol["momentum"].iloc[-1] + df_symbol["slope"].iloc[-1]

    scores.append({
        "symbol": symbol,
        "score": score,
    })

# 🔢 Rank & Allocate
if not scores:
    print("❌ No eligible symbols for scoring. Try fetching more historical data.")
    exit(1)

df_scores = pd.DataFrame(scores)
df_scores = df_scores.sort_values(by="score", ascending=False)
top = df_scores.head(1)["symbol"].values.tolist()

# 📊 Sacred Allocation Output
allocation = {symbol: 100.0 / len(top) for symbol in top}
allocation["CASH"] = 0.0

# 💾 Save Results
GOALS_PATH.parent.mkdir(parents=True, exist_ok=True)
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
STRATEGY_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

with open(GOALS_PATH, "w", encoding="utf-8") as f:
    json.dump(allocation, f, indent=2)

with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(f"[{datetime.now()}] Allocation: {allocation}\n")

with open(STRATEGY_LOG_PATH, "a", encoding="utf-8") as f:
    f.write(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "scores": scores,
        "top_pick": top,
        "allocation": allocation
    }) + "\n")

# 🧘 Completion
print("\n📊 Judas Strategy Engine Output (Dynamic Allocation):")
for symbol, weight in allocation.items():
    print(f"{symbol}: {weight:.2f}%")

print("\n✅ Allocation saved to", GOALS_PATH)
print("📁 Diagnostics saved to", LOG_PATH)
print("📜 Strategy log appended to", STRATEGY_LOG_PATH)
print("🧠 Powered by Judas — fully data-driven.")
