import json
import os


class MemoryEngine:

    def __init__(self, path="memory.json"):
        self.path = path
        self.memory = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return {}

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def _save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.memory, f)
        except:
            pass

    def learn(self, items):

        for item in items:

            topic = str(item.get("topic", "")).lower()

            if not topic:
                continue

            if topic not in self.memory:
                self.memory[topic] = {
                    "count": 0,
                    "total_score": 0
                }

            self.memory[topic]["count"] += 1
            self.memory[topic]["total_score"] += item.get("score", 1.0)

        self._save()

    def boost(self, items):

        for item in items:

            topic = str(item.get("topic", "")).lower()

            if topic in self.memory:
                data = self.memory[topic]
                avg = data["total_score"] / max(data["count"], 1)
                item["score"] += avg * 0.3

        return items
