from ib_insync import IB

def fetch_real_portfolio():
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)  # Connect to live account
    positions = ib.positions()

    mirrored = []
    for pos in positions:
        mirrored.append({
            'symbol': pos.contract.symbol,
            'quantity': pos.position,
            'avgCost': pos.avgCost
        })

    ib.disconnect()

    with open('real_portfolio.json', 'w') as f:
        import json
        json.dump(mirrored, f, indent=2)

    print("✅ Real portfolio mirrored to 'real_portfolio.json'")

if __name__ == "__main__":
    fetch_real_portfolio()
