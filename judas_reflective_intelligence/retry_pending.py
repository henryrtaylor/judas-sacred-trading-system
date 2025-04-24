import os
import httpx
from dotenv import load_dotenv
from phase15_cap_sym.log_to_sheet import log_to_sheet

load_dotenv()
LIGHTHOUSE_KEY = os.getenv("LIGHTHOUSE_KEY", "").strip()
pending_folder = "logs/pending_uploads"

def upload_to_lighthouse(file_path):
    headers = {
        "Authorization": f"Bearer {LIGHTHOUSE_KEY}"
    }
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "application/octet-stream")}
        with httpx.Client(http2=True, verify=True, timeout=30.0) as client:
            response = client.post("https://node.lighthouse.storage/api/v0/add", headers=headers, files=files)
    if response.status_code == 200 and "Hash" in response.json():
        return response.json()["Hash"]
    else:
        raise Exception(f"Lighthouse upload failed: {response.text}")

def retry_all_pending():
    print("🔁 RETRYING PENDING ARCHIVES...")
    if not os.path.exists(pending_folder):
        print("📭 No pending uploads found.")
        return

    for fname in os.listdir(pending_folder):
        fpath = os.path.join(pending_folder, fname)
        if not fname.endswith(".csv"):
            continue
        label = fname.split("__")[0].replace("_", " ").upper()
        try:
            cid = upload_to_lighthouse(fpath)
            url = f"https://gateway.lighthouse.storage/ipfs/{cid}"
            log_to_sheet("archive_logs", action="RETRY_UPLOAD", symbol=label, outcome=cid, notes=url)
            print(f"✅ Re-uploaded {fname} → {url}")
            os.remove(fpath)
        except Exception as e:
            print(f"❌ Failed retry for {fname}: {e}")

if __name__ == "__main__":
    retry_all_pending()