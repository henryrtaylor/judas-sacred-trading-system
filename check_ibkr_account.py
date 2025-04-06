# check_ibkr_account.py

from broker_adapter import IBKRAdapter
from judas_config import CONFIG
from pprint import pprint

def main():
    print("🔌 Connecting to IBKR...")
    adapter = IBKRAdapter(config=CONFIG)
    try:
        summary = adapter.get_account_summary()
        print("\n📊 Live Account Summary:")
        pprint(summary)
    except Exception as e:
        print("❌ Failed to retrieve account info:", e)

if __name__ == "__main__":
    main()