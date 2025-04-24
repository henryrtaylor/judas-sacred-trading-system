import os
import json
from datetime import datetime
from sentence_transformers import SentenceTransformer

class MobiusLogger:
    def __init__(self, model_name='all-MiniLM-L6-v2', path='21_mimic/mobius_memory.json'):
        self.model = SentenceTransformer(model_name)
        self.path = path
        if not os.path.exists(path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def store(self, text, source, tags=None):
        embedding = self.model.encode(text).tolist()
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "text": text,
            "source": source,
            "tags": tags or [],
            "embedding": embedding
        }
        with open(self.path, "r+") as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
        print("🧠 Mobius memory stored.")