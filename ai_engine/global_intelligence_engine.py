# ai_engine/global_intelligence_engine.py

from datetime import datetime


class GlobalIntelligenceEngine:

    def __init__(self):
        self.history = []
        self.max_history = 300

    # -------------------------
    # MAIN
    # -------------------------
    def process(self, intelligence):

        if not intelligence:
            return []

        enhanced = []

        for item in intelligence:

            if not isinstance(item, dict):
                continue

            topic = str(item.get("topic", "")).strip()
            if len(topic) < 5:
                continue

            score = self._safe_float(item.get("score", 1.0))

            category = self._categorize(topic)
            actors = self._extract_actors(topic)
            risk = self._compute_risk(score, topic)
            trend = self._compute_trend(topic, score)
            importance = self._importance(score, risk)

            enriched = {
                "topic": topic,
                "score": round(score, 2),
                "category": category,
                "actors": actors,
                "risk": risk,
                "trend": trend,
                "importance": importance,
                "summary": self._build_summary(topic, category, risk, trend),
                "timestamp": self._now()
            }

            enhanced.append(enriched)

        # memory update
        self.history.extend(enhanced)
        self.history = self.history[-self.max_history:]

        return enhanced

    # -------------------------
    # CATEGORY
    # -------------------------
    def _categorize(self, topic):

        t = topic.lower()

        if any(x in t for x in ["war", "attack", "military", "missile", "conflict"]):
            return "geopolitics"

        if any(x in t for x in ["ai", "technology", "robot", "openai", "spacex"]):
            return "technology"

        if any(x in t for x in ["bank", "economy", "market", "billion", "ipo"]):
            return "economy"

        if any(x in t for x in ["election", "government", "law", "court"]):
            return "politics"

        return "general"

    # -------------------------
    # ACTORS
    # -------------------------
    def _extract_actors(self, topic):

        words = topic.split()
        actors = []

        for w in words:
            if w.istitle() and len(w) > 3:
                actors.append(w)

        return list(set(actors))[:5]

    # -------------------------
    # RISK ENGINE
    # -------------------------
    def _compute_risk(self, score, topic):

        t = topic.lower()
        risk = score

        if any(x in t for x in ["war", "attack", "crisis", "explosion"]):
            risk += 3

        if any(x in t for x in ["collapse", "bankrupt", "failure"]):
            risk += 2

        return min(risk, 10)

    # -------------------------
    # TREND ENGINE
    # -------------------------
    def _compute_trend(self, topic, score):

        past_scores = [
            h["score"]
            for h in self.history
            if topic[:40] in h.get("topic", "")
        ]

        if not past_scores:
            return "new"

        avg = sum(past_scores) / len(past_scores)

        if score > avg * 1.4:
            return "surging"
        elif score < avg * 0.7:
            return "declining"
        else:
            return "stable"

    # -------------------------
    # IMPORTANCE
    # -------------------------
    def _importance(self, score, risk):

        val = score + risk

        if val > 12:
            return "critical"
        elif val > 8:
            return "high"
        elif val > 5:
            return "medium"
        return "low"

    # -------------------------
    # SUMMARY
    # -------------------------
    def _build_summary(self, topic, category, risk, trend):

        return f"{category.upper()} | {topic} | risk={risk} | trend={trend}"

    # -------------------------
    # UTILS
    # -------------------------
    def _safe_float(self, x, default=1.0):
        try:
            return float(x)
        except:
            return default

    def _now(self):
        return datetime.utcnow().isoformat()
