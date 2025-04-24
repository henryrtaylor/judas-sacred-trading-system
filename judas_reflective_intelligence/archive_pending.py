import os
import shutil
from datetime import datetime

def archive_pending(file_path, label):
    try:
        pending_dir = "logs/pending_uploads"
        os.makedirs(pending_dir, exist_ok=True)
        base = os.path.basename(file_path)
        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        new_name = f"{label.replace(' ', '_').lower()}__{timestamp}.csv"
        target = os.path.join(pending_dir, new_name)
        shutil.copy(file_path, target)
        print(f"📥 Archived to pending folder: {target}")
        return target
    except Exception as e:
        print(f"❌ Failed to store pending archive: {e}")