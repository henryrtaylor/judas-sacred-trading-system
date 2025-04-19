import os
import httpx
from datetime import datetime
from dotenv import load_dotenv
from phase15_cap_sym.log_to_sheet import log_to_sheet

load_dotenv()
LIGHTHOUSE_KEY = os.getenv("LIGHTHOUSE_KEY", "").strip()

LOG_FILES = [
    ("logs/rebalance_logs.csv", "REBALANCE LOG"),
    ("logs/paper_trades.csv", "PAPER TRADES"),
    ("logs/equity_curve.csv", "EQUITY CURVE")
]

def upload_to_lighthouse(file_path):
    headers = {
        "Authorization": f"Bearer {LIGHTHOUSE_KEY}"
    }
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "application/octet-stream")}
        with httpx.Client(http2=True, verify=True, timeout=30.0) as client:
            response = client.post("https://node.lighthouse.storage/api/v0/add", headers=headers, files=files)
    if response.status_code == 200 and "Hash" in response.json():
        cid = response.json()["Hash"]
        return cid
    else:
        raise Exception(f"Lighthouse upload failed: {response.text}")

def archive_and_log(file_path, label):
    try:
        filename = os.path.basename(file_path)
        user_input = input(f"🕯️ Judas is about to upload '{filename}' to Lighthouse. Proceed? (y/n): ").strip().lower()
        if user_input != 'y':
            print(f"⛔ Upload for {label} cancelled by user.")
            log_to_sheet("archive_logs", action="SKIPPED", symbol=label, outcome="CANCELLED", notes="User declined archive.")
            return

        cid = upload_to_lighthouse(file_path)
        url = f"https://gateway.lighthouse.storage/ipfs/{cid}"
        log_to_sheet("archive_logs", action="UPLOAD", symbol=label, outcome=cid, notes=url)
        print(f"✅ Archived {label} → {url}")
    except Exception as e:
        print(f"❌ Failed to archive {label}: {e}")

if __name__ == "__main__":
    print("🕯️ ARCHIVING TO LIGHTHOUSE STARTED (APPROVAL MODE)...")
    for file_path, label in LOG_FILES:
        if os.path.exists(file_path):
            archive_and_log(file_path, label)
        else:
            print(f"⚠️ {file_path} not found – skipping.")
    print("📜 ARCHIVING COMPLETE.")