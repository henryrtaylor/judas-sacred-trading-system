from datetime import date

FOMC_DATES = [
    "2025-03-19", "2025-05-07", "2025-06-18", "2025-07-30",
    "2025-09-17", "2025-11-05", "2025-12-17"
]

def is_fomc_day():
    today = date.today().strftime("%Y-%m-%d")
    return today in FOMC_DATES
