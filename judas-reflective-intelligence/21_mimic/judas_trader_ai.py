import requests
import datetime

class JudasTraderAI:
    def __init__(self):
        self.source = "https://api.pushshift.io/reddit/search/submission/?subreddit=wallstreetbets&sort=desc&size=10"

    def observe(self):
        print(f"📡 [{datetime.datetime.utcnow()}] Observing trader activity...")
        try:
            response = requests.get(self.source)
            data = response.json()["data"]
            results = []
            for post in data:
                title = post.get("title", "")
                url = post.get("full_link", "")
                score = post.get("score", 0)
                created = datetime.datetime.utcfromtimestamp(post.get("created_utc", 0))
                results.append((created, title[:100], score, url))
                print(f"🧠 {created} | {score} pts\n   {title[:100]}\n   ↪ {url}\n")
            return results
        except Exception as e:
            print(f"❌ Observation failed: {e}")
            return []

if __name__ == "__main__":
    ai = JudasTraderAI()
    ai.observe()