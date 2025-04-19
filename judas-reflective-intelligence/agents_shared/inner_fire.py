import json
from datetime import datetime

class InnerFire:
    def __init__(self, agent_name, log_path=None):
        self.agent_name = agent_name
        self.log_path = log_path or f"agents/{agent_name}/evolution_log.json"
        self._init_log()

    def _init_log(self):
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w") as f:
                json.dump([], f)

    def ignite(self, result, source, lesson, promise, score=None):
        log = {
            "cycle": datetime.utcnow().isoformat(),
            "source": source,
            "result": result,
            "lesson": lesson,
            "promise": promise,
            "score": score
        }
        with open(self.log_path, "r+") as f:
            data = json.load(f)
            data.append(log)
            f.seek(0)
            json.dump(data, f, indent=2)
        print(f"🔥 Inner fire log saved for {self.agent_name}")

    def review(self, n=3):
        with open(self.log_path, "r") as f:
            data = json.load(f)
        print(f"🧠 Last {n} reflections from {self.agent_name}:")
        for entry in data[-n:]:
            print(f"- {entry['cycle']} | {entry['lesson']} → {entry['promise']}")