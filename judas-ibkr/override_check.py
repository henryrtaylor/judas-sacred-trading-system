import time
import os

def check_override(seconds=7, flag_path="override/stop.txt"):
    print(f"⏳ Override window: {seconds} seconds...")
    time.sleep(seconds)

    if os.path.exists(flag_path):
        print("⛔ Override detected. Action aborted.")
        return False

    print("✅ No override detected. Proceeding...")
    return True

if __name__ == "__main__":
    check_override()