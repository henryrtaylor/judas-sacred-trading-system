
# broker_adapter.py
from abc import ABC, abstractmethod

class BrokerAdapter(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def get_account_summary(self):
        pass

    @abstractmethod
    def get_positions(self):
        pass

    @abstractmethod
    def get_open_orders(self):
        pass

    def place_order(self, symbol, qty, side, type='market'):
        raise NotImplementedError("Trading not enabled in read-only mode.")


class IBKRAdapter(BrokerAdapter):
    def __init__(self, config):
        super().__init__(config)
        from ib_insync import IB
        self.ib = IB()
        self.ib.connect(
            config.get("ib_host", "127.0.0.1"),
            int(config.get("ib_port", 7497)),
            int(config.get("ib_client_id", 1))
        )

    def get_account_summary(self):
        summary_items = self.ib.accountSummary()
        summary_dict = {}
        for item in summary_items:
            try:
                summary_dict[item.tag] = float(item.value)
            except ValueError:
                summary_dict[item.tag] = item.value

        return {
            "equity": summary_dict.get("NetLiquidation", 0.0),
            "cash": summary_dict.get("AvailableFunds", 0.0),
            "buying_power": summary_dict.get("BuyingPower", 0.0),
            "status": "connected" if self.ib.isConnected() else "disconnected"
        }

    def get_positions(self):
        positions = self.ib.positions()
        return [{
            "symbol": p.contract.symbol,
            "qty": p.position,
            "avg_cost": getattr(p, 'avgCost', 0.0),
            "unrealized_pl": getattr(p, 'unrealizedPNL', 0.0)
        } for p in positions]

    def get_open_orders(self):
        open_orders = self.ib.openOrders()
        return [{
            "symbol": o.contract.symbol,
            "qty": o.totalQuantity,
            "side": o.action,
            "type": o.orderType,
            "status": "open"
        } for o in open_orders]
