class GlobalIntelligenceEngine:

    def __init__(self):
        self.history = []
        self.max_history = 200

    # -------------------------
    # MAIN PROCESS
    # -------------------------
    def process(self, intelligence):

        if not intelligence or not isinstance(intelligence, list):
            return []

        cleaned = self._deduplicate(intelligence)

        enhanced = []

        for item in cleaned:

            if not isinstance(item, dict):
                continue

            topic = str(item.get("topic", "")).strip()
            if len(topic) < 5:
                continue

            score = self._safe_float(item.get("score", 1.0))

            summary = item.get("summary")
            if not summary:
                summary = self._generate_summary(topic)

            trend = self._compute_trend(topic, score)

            enriched = {
                "topic": topic,
                "summary": summary,
                "trend": trend,
                "score": round(score, 2),
                "importance": self._compute_importance(score),
                "timestamp": self._now()
            }

            enhanced.append(enriched)

        # HISTORY UPDATE
        self.history.extend(enhanced)
        self.history = self.history[-self.max_history:]

        return enhanced

    # -------------------------
    # 🔥 DUPLICATE CLEAN
    # -------------------------
    def _deduplicate(self, items):

        seen = set()
        result = []

        for item in items:

            topic = str(item.get("topic", "")).lower().strip()
            key = topic[:80]

            if key in seen:
                continue

            seen.add(key)
            result.append(item)

        return result

    # -------------------------
    # 🔥 TREND DETECTION
    # -------------------------
    def _compute_trend(self, topic, score):

        past_scores = [
            h["score"] for h in self.history
            if topic[:50] in h.get("topic", "")
        ]

        if not past_scores:
            return "new"

        avg = sum(past_scores) / len(past_scores)

        if score > avg * 1.3:
            return "rising"
        elif score < avg * 0.7:
            return "falling"
        else:
            return "stable"

    # -------------------------
    # 🔥 SUMMARY GENERATOR
    # -------------------------
    def _generate_summary(self, topic):

        words = topic.split()

        if len(words) <= 6:
            return f"Emerging signal around {topic}"

        return " ".join(words[:10])

    # -------------------------
    # 🔥 IMPORTANCE LOGIC (UPGRADED)
    # -------------------------
    def _compute_importance(self, score):

        if score >= 8:
            return "critical"
        elif score >= 5:
            return "high"
        elif score >= 3:
            return "medium"
        else:
            return "low"

    # -------------------------
    # SAFE FLOAT
    # -------------------------
    def _safe_float(self, x, default=1.0):
        try:
            return float(x)
        except:
            return default

    # -------------------------
    # TIME
    # -------------------------
    def _now(self):
        from datetime import datetime
        return datetime.utcnow().isoformat()
