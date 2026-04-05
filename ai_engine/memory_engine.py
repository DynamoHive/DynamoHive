import json
import os


class MemoryEngine:

    def __init__(self, path="memory.json"):
        self.path = path
        self.memory = self._load()

    # -------------------------
    # LOAD (SAFE)
    # -------------------------
    def _load(self):
        if not os.path.exists(self.path):
            return {}

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    # -------------------------
    # SAVE (SAFE + ATOMIC)
    # -------------------------
    def _save(self):
        try:
            tmp_path = self.path + ".tmp"

            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, ensure_ascii=False)

            os.replace(tmp_path, self.path)

        except Exception:
            pass

    # -------------------------
    # NORMALIZE
    # -------------------------
    def _normalize(self, topic):
        if not topic:
            return None
        return str(topic).strip().lower()

    # -------------------------
    # SAFE SCORE
    # -------------------------
    def _safe_score(self, value):
        try:
            return float(value)
        except Exception:
            return 1.0

    # -------------------------
    # LEARN
    # -------------------------
    def learn(self, items):

        if not isinstance(items, list):
            return

        for item in items:

            if not isinstance(item, dict):
                continue

            topic = self._normalize(item.get("topic"))
            if not topic:
                continue

            score = self._safe_score(item.get("score", 1.0))

            if topic not in self.memory:
                self.memory[topic] = {
                    "count": 0,
                    "total_score": 0.0
                }

            self.memory[topic]["count"] += 1
            self.memory[topic]["total_score"] += score

        self._save()

    # -------------------------
    # BOOST
    # -------------------------
    def boost(self, items):

        if not isinstance(items, list):
            return items

        for item in items:

            if not isinstance(item, dict):
                continue

            topic = self._normalize(item.get("topic"))
            if not topic:
                continue

            score = self._safe_score(item.get("score", 1.0))

            if topic in self.memory:
                data = self.memory[topic]

                count = data.get("count", 1)
                total = data.get("total_score", 1.0)

                avg = total / max(count, 1)

                # kontrollü boost (patlamaz)
                boost = min(avg * 0.3, 3)

                score += boost

            item["score"] = round(score, 3)

        return items
