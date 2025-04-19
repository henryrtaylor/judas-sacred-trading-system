from datetime import datetime

def get_time_window():
    now = datetime.now()
    hour = now.hour

    if hour < 9:
        return "Pre-Market"
    elif 9 <= hour < 16:
        return "Market Hours"
    else:
        return "After Hours"

def is_morning_scan_time():
    now = datetime.now()
    return now.hour == 8 and now.minute >= 45  # 8:45 AM
