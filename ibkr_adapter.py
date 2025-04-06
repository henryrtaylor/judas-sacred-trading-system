
class IBKRAdapter:
    def __init__(self, config):
        self.config = config

    def get_positions(self):
        # Mocked data
        return [
            {"symbol": "AAPL", "qty": 10, "avg_price": 175.25},
            {"symbol": "TSLA", "qty": 5, "avg_price": 850.75}
        ]
