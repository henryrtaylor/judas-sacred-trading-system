# config.py

# === ACCOUNT SWITCH ===
USE_LIVE_TRADING = False  # 🔁 Set to True to enable live trading

# === CONNECTION SETTINGS ===
IBKR_HOST = '127.0.0.1'
IBKR_PORT = 7497 if USE_LIVE_TRADING else 7496  # 7497 = Live / 7496 = Paper
CLIENT_ID = 1

# === SAFETY ===
MIN_ORDER_DOLLARS = 25     # Avoid micro orders
MAX_ORDER_DOLLARS = 2000   # Never risk more than this per order (you can change)
