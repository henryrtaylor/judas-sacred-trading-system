import os
import csv
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from ipfs_uploader import upload_to_ipfs

SHEET_ID = "1zDmZPAX_dG_NjAHXNbN8n82EINJxzI9DQczBXZpVq2k"
CREDS_PATH = os.getenv("JUDAS_SHEETS_CREDS", "config/judas-sheets-creds.json")
EXPORT_DIR = "logs"

TABS = ["rebalance_logs", "judgment_logs", "risk_alerts", "execution_logs", "equity_curve", "paper_trades", "live_trades"]

def get_worksheet(tab):
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID)
    return sheet.worksheet(tab)

def archive_and_clear(tab):
    try:
        ws = get_worksheet(tab)
        rows = ws.get_all_values()
        if not rows or len(rows) <= 1:
            print(f"⚠️ No data in {tab} to archive.")
            return
        timestamp = datetime.utcnow().strftime('%Y-%m')
        out_path = os.path.join(EXPORT_DIR, timestamp)
        os.makedirs(out_path, exist_ok=True)
        csv_file = os.path.join(out_path, f"{tab}.csv")
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print(f"✅ Archived {tab} to {csv_file}")
        ipfs_cid = upload_to_ipfs(csv_file)
        print(f"📡 Uploaded to IPFS: {ipfs_cid}")
        headers = rows[0]
        ws.clear()
        ws.append_row(headers)
        print(f"🧹 Cleared data from {tab}")
    except Exception as e:
        print(f"❌ Failed to archive {tab}: {e}")

if __name__ == "__main__":
    for tab in TABS:
        archive_and_clear(tab)