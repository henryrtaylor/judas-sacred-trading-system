import pandas as pd
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

# === CONFIGURATION ===
PORTFOLIO_FILE = "logs/portfolio_snapshot.csv"
ALLOCATION_FILE = "generated/generated_goals.json"
STRATEGY_LOG_FILE = "logs/judas_strategy_log.json"
SIM_LOG_FILE = "logs/judas_simulation_log.json"
MAX_VOLATILITY = 0.40
TRANSACTION_FEE = 1.00
SLIPPAGE_RATE = 0.0025
CASH_BUFFER_PCT = 0.10
REBALANCE_EXECUTE_SCRIPT = "rebalance_execute.py"

# === LOAD DATA ===
try:
    portfolio = pd.read_csv(PORTFOLIO_FILE)
    with open(ALLOCATION_FILE, 'r') as f:
        target_alloc = json.load(f)
except Exception as e:
    print(f"❌ Failed to load data: {e}")
    exit()

if 'CASH' not in target_alloc:
    target_alloc['CASH'] = 0.0  # fallback

# Adjust allocations to retain cash buffer
scalable_alloc = {k: v for k, v in target_alloc.items() if k != 'CASH'}
total_scalable = sum(scalable_alloc.values())
scaling_factor = 1 - CASH_BUFFER_PCT
adjusted_alloc = {k: round((v / total_scalable) * scaling_factor, 4) for k, v in scalable_alloc.items()}
adjusted_alloc['CASH'] = round(1 - sum(adjusted_alloc.values()), 4)

# Load latest strategy scores (with volatility info)
try:
    with open(STRATEGY_LOG_FILE, 'r') as f:
        strategy_history = json.load(f)
        latest_scores = strategy_history[-1]['scores']
        volatility_map = {row['symbol']: row.get('volatility', 0.0) for row in latest_scores}
except Exception as e:
    print(f"⚠️ Could not load volatility scores: {e}")
    volatility_map = {}

# === STRATEGY COMPARISON ===
print("\n📊 Strategy Comparison (Last 3 Allocations):")
try:
    with open(STRATEGY_LOG_FILE, 'r') as f:
        hist = json.load(f)
        recent = hist[-3:] if len(hist) >= 3 else hist
        for i, entry in enumerate(recent):
            alloc = entry.get('alloc', {})
            label = f"Run {len(hist)-len(recent)+i+1}"
            summary = ", ".join([f"{k}: {v:.0%}" for k, v in alloc.items()])
            print(f"{label:<8}: {summary}")
except Exception as e:
    print(f"⚠️ Could not compare strategies: {e}")

total_value = portfolio['est_value'].sum()
portfolio = portfolio.fillna(0)
portfolio_map = {row.symbol: row.est_value for row in portfolio.itertuples()}

# === SIMULATION ===
orders = []
summary = {
    "total_value": round(total_value, 2),
    "rebalancing": []
}

print("\n🧪 Judas Simulation Summary")
print(f"💼 Portfolio Value: ${total_value:,.2f}")
print(f"💵 Cash Reserve Set Aside: {CASH_BUFFER_PCT:.0%}\n")
print("🧾 Rebalancing Orders:")

for symbol, weight in adjusted_alloc.items():
    volatility = volatility_map.get(symbol, 0.0)
    if symbol != 'CASH' and volatility > MAX_VOLATILITY:
        print(f"⚠️ Skipping {symbol}: volatility {volatility:.2%} exceeds threshold {MAX_VOLATILITY:.0%}")
        orders.append({
            "symbol": symbol,
            "current_value": portfolio_map.get(symbol, 0.0),
            "target_value": 0.0,
            "difference": 0.0,
            "action": "hold",
            "commentary": f"Skipped due to high volatility ({volatility:.2%})"
        })
        continue

    target_value = weight * total_value
    current_value = portfolio_map.get(symbol, 0.0)
    delta = round(target_value - current_value, 2)
    direction = "buy" if delta > 0 else "sell" if delta < 0 else "hold"

    # Fee/Slippage Adjustments
    fee = TRANSACTION_FEE
    slippage = abs(delta) * SLIPPAGE_RATE
    adjusted_delta = abs(delta) - (fee + slippage)

    if adjusted_delta <= 0 or direction == "hold":
        commentary = f"{symbol} trade skipped after accounting for fee (${fee:.2f}) and slippage (${slippage:.2f})."
        print(f"⚠️ HOLD  {symbol}  // {commentary}")
        orders.append({
            "symbol": symbol,
            "current_value": round(current_value, 2),
            "target_value": round(target_value, 2),
            "difference": 0.0,
            "action": "hold",
            "volatility": volatility,
            "commentary": commentary
        })
        continue

    adjusted_delta = round(adjusted_delta, 2)
    net_direction = direction
    commentary = f"{direction.title()} ${adjusted_delta:,.2f} of {symbol} after fees/slippage. (raw delta: ${abs(delta):,.2f})"

    print(f"➡️ {net_direction.upper():<4} ${adjusted_delta:,.2f} of {symbol}  // {commentary}")
    orders.append({
        "symbol": symbol,
        "current_value": round(current_value, 2),
        "target_value": round(target_value, 2),
        "difference": adjusted_delta if direction == "buy" else -adjusted_delta,
        "action": net_direction,
        "volatility": volatility,
        "commentary": commentary
    })

    summary["rebalancing"].append({"symbol": symbol, "action": net_direction, "amount": adjusted_delta})

# === SAVE LOG ===
Path("logs").mkdir(exist_ok=True)
log_entry = {
    "timestamp": datetime.now().isoformat(),
    "simulation": orders,
    "summary": summary
}

try:
    if Path(SIM_LOG_FILE).exists():
        with open(SIM_LOG_FILE, "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append(log_entry)
    with open(SIM_LOG_FILE, "w") as f:
        json.dump(history, f, indent=2)

    print(f"\n✅ Simulation saved to {SIM_LOG_FILE}")
except Exception as e:
    print(f"⚠️ Failed to write simulation log: {e}")

# === AUTO-EXECUTE ===
print("\n⏳ Auto-execution in 10 seconds. Press Ctrl+C to cancel.")
try:
    for i in range(10, 0, -1):
        print(f"...{i}", end=" ", flush=True)
        time.sleep(1)
    print("\n🚀 Executing Judas' plan...")
    subprocess.run(["python", REBALANCE_EXECUTE_SCRIPT])
except KeyboardInterrupt:
    print("\n❌ Execution cancelled by user.")
