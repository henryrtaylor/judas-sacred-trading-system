from consensus_engine import get_consensus_signals
from rss_nlp_listener import get_nlp_signals
from micro_signal_engine import get_micro_signals

def get_all_signals(watchlist, data_cache):
    signals = {}
    for symbol in watchlist:
        signals[symbol] = {
            "consensus": get_consensus_signals(symbol, data_cache.get(symbol)),
            "nlp": get_nlp_signals(symbol),
            "micro": get_micro_signals(symbol, data_cache.get(symbol))
        }
    return signals