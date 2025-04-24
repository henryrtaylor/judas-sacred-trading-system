
# nlp_shadow_runner.py

import json
from datetime import datetime
from mock_nlp_signal_engine import interpret_headline
from trade_logger import TradeLogger
from trade_executor import TradeExecutor

def run_nlp_shadow_session(headlines_path, broker_adapter, config=None):
    logger = TradeLogger(log_path='logs/trade_journal_nlp.json')
    executor = TradeExecutor(broker_adapter, trade_logger=logger, read_only=True, config=config)

    with open(headlines_path, 'r') as f:
        headlines = json.load(f)

    signals = []

    for item in headlines:
        result = interpret_headline(item['headline'])
        signals.append(result)

        if result["signal"] in ["BUY", "SELL"]:
            executor.execute_trade(
                result["symbol"], 1, result["signal"], 
                f"NLP: {result['reason']}"
            )

    with open("logs/nlp_signals.json", "w") as f:
        json.dump(signals, f, indent=2)

    print(f"✅ NLP session complete. {len(signals)} headlines processed.")
