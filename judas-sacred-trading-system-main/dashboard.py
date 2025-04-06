import csv
from collections import defaultdict
from pathlib import Path

TRADE_LOG = Path("logs/trades.csv")

if not TRADE_LOG.exists():
    print("🚫 No trade log found. Place a trade first!")
    exit()

trades = []

with open(TRADE_LOG, mode='r') as f:
    reader = csv.reader(f)
    for row in reader:
        trades.append({
            'time': row[0],
            'symbol': row[1],
            'type': row[2],
            'action': row[3],
            'qty': float(row[4]),  # ✅ Fixed: use float instead of int
            'price': float(row[5]) if row[5] != 'N/A' else None,
            'status': row[6]
        })

print("\n📊 --- Trade Summary Dashboard ---")

print(f"📈 Total Trades: {len(trades)}")
symbols = set(t['symbol'] for t in trades)
print(f"🔢 Symbols Traded: {', '.join(symbols)}")

total_qty = sum(t['qty'] for t in trades)
filled_trades = [t for t in trades if t['price']]
avg_price = round(sum(t['price'] * t['qty'] for t in filled_trades) / total_qty, 4)
print(f"📦 Total Volume: {total_qty}")
print(f"💰 Avg Fill Price: {avg_price}")
avg_price = round(sum(t['price'] * t['qty'] for t in filled_trades) / total_qty, 4)

