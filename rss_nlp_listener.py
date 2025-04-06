# rss_nlp_listener.py

import time
import feedparser
import json
from datetime import datetime
from mock_nlp_signal_engine import interpret_headline
from trade_logger import TradeLogger
from nlp_trade_executor import NLPTradeExecutor
from socket_emitter import emit_socket

RSS_FEEDS = [
    "https://www.marketwatch.com/rss/topstories",
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US",
    "http://feeds.reuters.com/reuters/businessNews",
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://cointelegraph.com/rss"
]

def fetch_rss_headlines(feeds):
    headlines = []
    for feed_url in feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:10]:
            headlines.append({"headline": entry.title})
    return headlines

def run_rss_nlp_loop(config=None, interval_minutes=5):
    logger = TradeLogger(log_path='logs/trade_journal_nlp.json')
    executor = NLPTradeExecutor(logger, config=config)

    print(f"🔁 Starting RSS NLP Listener (interval: {interval_minutes} min)")
    while True:
        try:
            headlines = fetch_rss_headlines(RSS_FEEDS)
            signals = []

            for item in headlines:
                result = interpret_headline(item['headline'])
                signals.append(result)

                emit_socket({
                    "event": "nlp_signal",
                    "symbol": result.get("symbol"),
                    "signal": result.get("signal"),
                    "confidence": result.get("confidence"),
                    "reason": result.get("reason"),
                    "headline": item.get("headline"),
                    "timestamp": datetime.utcnow().isoformat()
                })

                if result["signal"] in ["BUY", "SELL"]:
                    executor.execute_trade(
                        result["symbol"], 1, result["signal"],
                        f"NLP: {result['reason']}"
                    )

            with open("logs/nlp_signals.json", "w") as f:
                json.dump(signals, f, indent=2)

            print(f"🗞️ Processed {len(signals)} headlines at {datetime.now().isoformat()}")
        except Exception as e:
            print(f"⚠️ Error in RSS NLP loop: {e}")

        time.sleep(interval_minutes * 60)