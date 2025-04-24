
# shadow_runner.py

from trade_logger import TradeLogger
from trade_executor import TradeExecutor
from signal_viewer import display_signals

def run_shadow_session(price_data, config, broker_adapter):
    logger = TradeLogger()
    executor = TradeExecutor(broker_adapter, trade_logger=logger, read_only=True)

    print("\n🕶️ Starting Shadow Mode Execution...")

    for symbol in config.get("watchlist", ["AAPL"]):
        for plugin_name, signal_fn in config["plugins"].items():
            try:
                signal_series = signal_fn(price_data)
                latest_signal = signal_series.dropna().iloc[-1]
                if latest_signal == 1:
                    executor.execute_trade(symbol, 1, "BUY", f"{plugin_name} signal +shadow")
                elif latest_signal == -1:
                    executor.execute_trade(symbol, 1, "SELL", f"{plugin_name} signal +shadow")
            except Exception as e:
                print(f"⚠️ Error in {plugin_name}: {e}")

    print("\n🧾 Session complete. Trades logged.")
