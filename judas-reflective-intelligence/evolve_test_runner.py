from evolve_agent import log_trade_result, summarize_strategy_performance

print("🧪 Simulating Evolution Log Entries...")

log_trade_result("SPY", "ai_solver", 0.82, "WIN", True)
log_trade_result("GLD", "momentum_agent", 0.74, "LOSS", True)
log_trade_result("BTC-USD", "reddit_agent", 0.66, "WIN", False)

print("\n🧬 Summary of Strategy Evolution:")
summarize_strategy_performance()