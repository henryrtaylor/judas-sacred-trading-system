import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

# Config
SHEET_ID = "1zDmZPAX_dG_NjAHXNbN8n82EINJxzI9DQczBXZpVq2k"
CREDS_PATH = os.getenv("JUDAS_SHEETS_CREDS", "config/judas-sheets-creds.json")
DEFAULT_HEADERS = ["timestamp", "mode", "symbol", "action", "size", "price", "reason", "agent", "notes"]

def get_worksheet(tab):
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID)

    try:
        ws = sheet.worksheet(tab)
    except gspread.exceptions.WorksheetNotFound:
        ws = sheet.add_worksheet(title=tab, rows="1000", cols="12")
        ws.append_row(DEFAULT_HEADERS)

    return ws

def log_trade(
    mode,           # "live" or "paper"
    symbol,
    action,         # "BUY", "SELL", "CLOSE"
    size,
    price,
    reason="",      # trade reason
    agent="Judas",
    notes=""
):
    assert mode in ("live", "paper"), "mode must be 'live' or 'paper'"
    tab = f"{mode}_trades"
    ws = get_worksheet(tab)
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    row = [timestamp, mode, symbol, action, size, price, reason, agent, notes]
    ws.append_row(row)
    print(f"✅ Logged {mode} trade to '{tab}':", row)