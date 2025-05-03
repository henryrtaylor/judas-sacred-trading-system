import asyncio
import pytest
from judas_ibkr.rebalancer import Rebalancer

# Dummy implementations for patches
async def dummy_fetch_ibkr_state(_ib):
    # Always $1,000 cash, no existing positions
    return 1000.0, {}

def dummy_generate_target_weights(prices, total, positions):
    # Equal weight on the first two symbols
    syms = list(prices.keys())[:2]
    return {syms[0]: 0.5, syms[1]: 0.5}

class DummyIB:
    def __init__(self):
        self.orders = []
    def place_order(self, sym, qty, price):
        self.orders.append((sym, qty, price))

@pytest.fixture(autouse=True)
def patch_dependencies(monkeypatch):
    # Patch fetch_ibkr_state
    import utils.broker_adapter as broker_adapter
    monkeypatch.setattr(broker_adapter, 'fetch_ibkr_state', dummy_fetch_ibkr_state)

    # Patch generate_target_weights
    import judas_reflective_intelligence.rebalance_scheduler_ai as rsai
    monkeypatch.setattr(rsai, 'generate_target_weights', dummy_generate_target_weights)

    # Patch safe_execute
    import judas_ibkr.safe_order as safe_order
    def fake_safe_execute(ib, sym, delta, price, _):
        ib.place_order(sym, delta, price)
    monkeypatch.setattr(safe_order, 'safe_execute', fake_safe_execute)

def test_execute_places_correct_orders():
    ib = DummyIB()
    reb = Rebalancer(watch_list=['AAA', 'BBB'], min_price_points=1, ib=ib)
    # Seed prices so no fallback fetch happens
    reb.prices['AAA'] = 10.0
    reb.prices['BBB'] = 20.0

    # Run the rebalance once
    asyncio.run(reb.execute())

    # Expect: AAA → 0.5*1000/10 = 50, BBB → 0.5*1000/20 = 25
    assert ('AAA', 50, 10.0) in ib.orders
    assert ('BBB', 25, 20.0) in ib.orders
    # No orders for symbols outside watch_list
    assert not any(o[0] == 'CCC' for o in ib.orders)

def test_execute_respects_existing_positions():
    ib = DummyIB()
    reb = Rebalancer(watch_list=['AAA', 'BBB'], min_price_points=1, ib=ib)
    reb.prices['AAA'] = 10.0
    reb.prices['BBB'] = 10.0

    # Override fetch_ibkr_state to return an existing 20‐share AAA position
    async def state2(_ib):
        return 1000.0, {'AAA': 20}
    import utils.broker_adapter as broker_adapter
    broker_adapter.fetch_ibkr_state = state2

    asyncio.run(reb.execute())

    # Portfolio = 1000 + (20*10) = 1200 → each target = 0.5*1200 = 600
    # AAA delta = 600/10 - 20 = 40; BBB delta = 600/10 = 60
    assert ('AAA', 40, 10.0) in ib.orders
    assert ('BBB', 60, 10.0) in ib.orders
