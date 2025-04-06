# micro_signal_engine.py
import yfinance as yf
import pandas as pd
from indicators import get_atr, rsi_signal


def get_micro_signals(symbol):
    try:
        data = yf.download(symbol, period="5d", interval="5m", progress=False)
        if data.empty:
            raise ValueError(f"No data found for {symbol}")

        # Basic ATR calculation to scale risk
        atr_series = get_atr(data)
        atr = atr_series.iloc[-1] if not atr_series.empty else 0

        # Example RSI signal
        rsi_decision = rsi_signal(data)

        # Dummy logic for confidence (can be extended with ML model or NLP)
        confidence = 1.0 if rsi_decision == "BUY" else 0.5 if rsi_decision == "NEUTRAL" else 0.2

        return {
            "symbol": symbol,
            "decision": rsi_decision,
            "confidence": confidence,
            "volatility": atr
        }

    except Exception as e:
        print(f"⚠️ Error in get_micro_signals({symbol}): {e}")
        return None


if __name__ == "__main__":
    from tabulate import tabulate

    print("\n📊 Micro Signal Self-Test Mode\n")
    test_symbols = ["AAPL", "TSLA"]
    results = []

    for sym in test_symbols:
        signal = get_micro_signals(sym)
        if signal:
            results.append([
                signal['symbol'],
                signal['decision'],
                f"{signal['confidence']:.2f}",
                f"{signal['volatility']:.2f}"
            ])

    print(tabulate(results, headers=["Symbol", "Decision", "Confidence", "ATR Volatility"], tablefmt="pretty"))
