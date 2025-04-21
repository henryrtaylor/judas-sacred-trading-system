
from judas_ibkr.ai_solver import ai_solver
import yfinance as yf

def run():
    symbols = ["SPY", "GLD", "BTC-USD"]
    price_data = {}
    for symbol in symbols:
        df = yf.download(symbol, period="90d", interval="1d")
        price_data[symbol] = df
    weights, refined = ai_solver(price_data)
    print("✅ AI Allocation Weights:", weights)

if __name__ == "__main__":
    run()
