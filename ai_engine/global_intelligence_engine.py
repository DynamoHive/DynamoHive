class GlobalIntelligenceEngine:

    def __init__(self):
        self.history = []

    def process(self, intelligence):

        if not intelligence:
            return []

        enhanced = []

        for item in intelligence:

            if not isinstance(item, dict):
                continue

            topic = item.get("topic", "unknown")
            summary = item.get("summary", "")
            trend = item.get("trend", "stable")
            score = item.get("score", 1.0)

            # 🔥 BASIC ENRICHMENT
            enriched = {
                "topic": topic,
                "summary": summary,
                "trend": trend,
                "score": score,
                "importance": self._compute_importance(score),
                "timestamp": self._now()
            }

            enhanced.append(enriched)

        self.history.extend(enhanced[-50:])

        return enhanced

    # -------------------------
    # 🔥 IMPORTANCE LOGIC
    # -------------------------
    def _compute_importance(self, score):

        try:
            score = float(score)
        except:
            score = 1.0

        if score > 5:
            return "critical"
        elif score > 3:
            return "high"
        elif score > 2:
            return "medium"
        else:
            return "low"

    # -------------------------
    # 🕒 TIME
    # -------------------------
    def _now(self):
        from datetime import datetime
        return datetime.utcnow().isoformat()
