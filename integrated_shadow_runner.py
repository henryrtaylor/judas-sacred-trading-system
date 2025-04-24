
# integrated_shadow_runner.py

from trade_logger import TradeLogger
from trade_executor import TradeExecutor
from signal_engine import get_plugin_signals, compute_consensus

def run_integrated_shadow_session(price_data_by_symbol, config, broker_adapter, threshold=2):
    logger = TradeLogger(log_path='logs/trade_journal_integrated.json')
    executor = TradeExecutor(broker_adapter, trade_logger=logger, read_only=True)

    print("\n🧠 Running Shadow Session with Consensus Engine...")

    for symbol in config.get("watchlist", []):
        if symbol not in price_data_by_symbol:
            print(f"⚠️ No data for symbol: {symbol}")
            continue

        df = price_data_by_symbol[symbol]
        plugin_signals = get_plugin_signals(df, config["plugins"])
        consensus = compute_consensus(plugin_signals, threshold=threshold)

        print(f"\n🔍 {symbol} Consensus: {consensus}")
        for name, sig in plugin_signals.items():
            print(f"  {name}: {sig['label']}")

        if consensus in ["BUY", "SELL"]:  # Only act if strong consensus
            executor.execute_trade(symbol, 1, consensus, f"Consensus: {consensus}")

    print("\n✅ Integrated Shadow Session complete.")
