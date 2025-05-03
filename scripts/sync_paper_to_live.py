from ib_insync import IB, Stock
import os

# Setup credentials and clients
LIVE_CLIENT_ID = int(os.getenv("LIVE_CLIENT_ID", "100"))
PAPER_CLIENT_ID = int(os.getenv("PAPER_CLIENT_ID", "101"))
IB_HOST = os.getenv("IBKR_HOST", "127.0.0.1")
IB_PORT = int(os.getenv("IBKR_API_PORT", "7497"))

print("🔁 Connecting to live account...")
live_ib = IB()
live_ib.connect(IB_HOST, IB_PORT, clientId=LIVE_CLIENT_ID)
live_acct = live_ib.managedAccounts()[0]
live_positions = {p.contract.symbol: p.position for p in live_ib.positions(live_acct)}
live_ib.disconnect()

print("📄 Connecting to paper account...")
paper_ib = IB()
paper_ib.connect(IB_HOST, IB_PORT, clientId=PAPER_CLIENT_ID)
paper_acct = paper_ib.managedAccounts()[0]
paper_positions = {p.contract.symbol: p.position for p in paper_ib.positions(paper_acct)}

# Sync logic
orders = []
for sym, live_qty in live_positions.items():
    delta = live_qty - paper_positions.get(sym, 0)
    if delta != 0:
        print(f"→ Adjust {sym}: {delta:+} shares")
        contract = Stock(sym, "SMART", "USD")
        action = "BUY" if delta > 0 else "SELL"
        order = paper_ib.marketOrder(action, abs(delta))
        paper_ib.placeOrder(contract, order)

paper_ib.disconnect()
print("✅ Paper account synchronized to match live holdings.")
