import os
import csv
import requests
from datetime import datetime
from dotenv import load_dotenv
from phase15_cap_sym.log_to_sheet import log_to_sheet

load_dotenv()

NFT_STORAGE_KEY = os.getenv("NFT_STORAGE_KEY", "").strip()
print("🔑 NFT Key Loaded:", NFT_STORAGE_KEY[:10], "...")  # Debug line

LOG_FILES = [
    ("logs/rebalance_logs.csv", "REBALANCE LOG"),
    ("logs/paper_trades.csv", "PAPER TRADES"),
    ("logs/equity_curve.csv", "EQUITY CURVE")
]

def upload_to_ipfs(file_path):
    headers = {
        "Authorization": f"Bearer {NFT_STORAGE_KEY}"
    }
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post("https://api.nft.storage/upload", headers=headers, files=files)
    if response.status_code == 200:
        cid = response.json()["value"]["cid"]
        return cid
    else:
        raise Exception(f"IPFS upload failed: {response.text}")

def archive_and_log(file_path, label):
    try:
        cid = upload_to_ipfs(file_path)
        url = f"https://{cid}.ipfs.nftstorage.link"
        log_to_sheet("archive_logs", action="UPLOAD", symbol=label, outcome=cid, notes=url)
        print(f"✅ Archived {label} → {url}")
    except Exception as e:
        print(f"❌ Failed to archive {label}: {e}")

if __name__ == "__main__":
    print("📤 ARCHIVING STARTED...")
    for file_path, label in LOG_FILES:
        if os.path.exists(file_path):
            archive_and_log(file_path, label)
        else:
            print(f"⚠️ {file_path} not found – skipping.")
    print("📜 ARCHIVING COMPLETE.")