from datetime import datetime

# Recognize market time segments and special days
def get_current_window():
    now = datetime.now()
    hour = now.hour

    if hour < 9:
        window = "Pre-Market"
    elif 9 <= hour < 16:
        window = "Market Hours"
    else:
        window = "After Hours"

    print(f"🕓 Market Window: {window}")
    return window
