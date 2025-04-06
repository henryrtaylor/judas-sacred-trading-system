import time
from signal_orchestrator import get_all_signals
from position_sizer import dynamic_allocation, scale_position

def run_scheduler(watchlist, interval=60):
    equity = 100000
    sentiment_index = 0.2
    confidence = 0.8
    volatility = 1.2

    while True:
        print("📡 Heartbeat")
        signals = get_all_signals(watchlist, {})
        allocation = dynamic_allocation(sentiment_index)
        position_size = scale_position(allocation, equity, confidence, volatility)
        print(f"💼 Position Size Estimate: {position_size:.2f}")
        time.sleep(interval)