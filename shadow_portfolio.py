
class ShadowPortfolio:
    def get_positions(self):
        return [
            {"symbol": "AAPL", "qty": 20, "avg_price": 173.50},
            {"symbol": "NVDA", "qty": 15, "avg_price": 270.10}
        ]

    def get_summary(self):
        return {
            "balance": 50000,
            "equity": 58000,
            "unrealized_pnl": 8000,
            "realized_pnl": 1200
        }
