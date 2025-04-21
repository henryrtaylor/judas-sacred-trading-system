import yaml

class RiskGuard:
    def __init__(self, config_path="risk_config.yml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def is_symbol_allowed(self, symbol, price):
        if not self.config.get("allow_all_symbols", False):
            return symbol not in self.config.get("blacklist_symbols", [])
        if symbol in self.config.get("blacklist_symbols", []):
            return False
        return self.config["min_price"] <= price <= self.config["max_price"]

    def get_risk_limits(self):
        return {
            "stop_loss_percent": self.config["stop_loss_percent"],
            "take_profit_percent": self.config["take_profit_percent"],
            "max_position_risk_percent": self.config["max_position_risk_percent"]
        }

    def print_summary(self):
        print("🛡️ Risk Limits and Blessings:")
        for k, v in self.get_risk_limits().items():
            print(f"- {k}: {v}%")

if __name__ == "__main__":
    rg = RiskGuard()
    rg.print_summary()
    print("Allowed symbol AAPL @ 170.5:", rg.is_symbol_allowed("AAPL", 170.5))
    print("Allowed symbol GME @ 18.2:", rg.is_symbol_allowed("GME", 18.2))