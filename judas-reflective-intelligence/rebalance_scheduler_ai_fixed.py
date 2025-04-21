import yfinance as yf
from ai_solver import ai_solver
from trade_executor import execute_order
import datetime

ASSETS = ['SPY', 'GLD', 'BTC-USD']

def fetch_price_data():
    data = {}
    for symbol in ASSETS:
        try:
            df = yf.download(symbol, period="90d", interval="1d")
            df = df[['Close']].rename(columns={'Close': 'close'})
            data[symbol] = df
        except Exception as e:
            print(f"❌ Failed to fetch {symbol}: {e}")
    return data

def simulate_allocation_and_execute():
    price_data_dict = fetch_price_data()
    weights = ai_solver(price_data_dict)

    for symbol, weight in weights.items():
        try:
            price = float(round(price_data_dict[symbol]['close'].iloc[-1], 2))
            size = round(weight * 10000 / price, 2)
            execute_order(symbol, size, side="BUY", price=price, mode="paper", context="AI Rebalance")
        except Exception as e:
            print(f"❌ Execution error for {symbol}: {e}")

if __name__ == "__main__":
    print(f"🔄 [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting AI-driven rebalance...")
    simulate_allocation_and_execute()
    print("✅ AI Rebalance complete.")