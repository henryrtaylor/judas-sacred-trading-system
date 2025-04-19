import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

# Config
SHEET_ID = "1zDmZPAX_dG_NjAHXNbN8n82EINJxzI9DQczBXZpVq2k"
CREDS_PATH = os.getenv("JUDAS_SHEETS_CREDS", "config/judas-sheets-creds.json")
DEFAULT_HEADERS = ["timestamp", "agent", "action", "symbol", "outcome", "notes"]

def get_worksheet(tab):
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID)

    try:
        ws = sheet.worksheet(tab)
    except gspread.exceptions.WorksheetNotFound:
        ws = sheet.add_worksheet(title=tab, rows="1000", cols="10")
        ws.append_row(DEFAULT_HEADERS)

    return ws

def log_to_sheet(tab, agent="Judas", action="", symbol="", outcome="", notes=""):
    ws = get_worksheet(tab)
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    row = [timestamp, agent, action, symbol, outcome, notes]
    ws.append_row(row)
    print(f"✅ Logged to '{tab}':", row)