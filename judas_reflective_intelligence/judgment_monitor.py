import time
from judgment_layer.zion_council import ZionCouncil

CHECK_INTERVAL = 7  # seconds

def check_agents():
    council = ZionCouncil()
    result = council.reflect("Periodic judgment check")
    timestamp = result.get("timestamp")
    score = result.get("alignment_score")
    consensus = result.get("consensus")

    if consensus and "NO" in consensus:
        print(f"⚠️ [{timestamp}] Irregular signals: alignment_score={score}, consensus={consensus}")
    else:
        print(f"✔ [{timestamp}] All agents aligned: alignment_score={score}, consensus={consensus}. Next check in {CHECK_INTERVAL}s.")

if __name__ == "__main__":
    print("🧠 Judgment Monitor starting…")
    while True:
        check_agents()
        time.sleep(CHECK_INTERVAL)
