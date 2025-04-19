from scheduler import get_time_window, is_morning_scan_time
from holy_days import is_fomc_day

def run_daily_logic():
    window = get_time_window()
    if window != "Pre-Market":
        print(f"⏰ Not in pre-market. Current window: {window}")
        return

    if not is_morning_scan_time():
        print("🕓 Not within the scan window (8:45 AM).")
        return

    if is_fomc_day():
        print("⚠️ FOMC Day detected. Tighten filters. Watch volatility.")
    else:
        print("✅ Standard morning conditions.")

    print("📡 Begin scan, signal generation, or daily report...")

if __name__ == "__main__":
    run_daily_logic()
