# utils/summary.py

def print_account_summary(summary):
    print("\n--- Account Summary ---")
    for item in summary:
        print(f"{item.tag:<25} {item.value} {item.currency}")
