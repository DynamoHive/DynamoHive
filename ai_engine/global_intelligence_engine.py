import re
from datetime import datetime


class GlobalIntelligenceEngine:

    def __init__(self):
        self.history = []
        self.max_history = 300

    def process(self, signals):

        if not signals:
            return []

        enhanced = []

        for s in signals:

            topic = str(s.get("topic", "")).strip()
            if len(topic) < 5:
                continue

            score = self._safe_float(s.get("score", 1.0))

            category = self._categorize(topic)
            insight = self._extract_insight(topic, category)
            risk = self._compute_risk(topic, score)
            trend = self._compute_trend(topic, score)

            enriched = {
                "topic": topic,
                "score": round(score, 2),
                "category": category,
                "insight": insight,
                "risk": risk,
                "trend": trend,
                "importance": self._importance(score, risk),
                "summary": self._build_summary(insight, risk),
                "timestamp": self._now()
            }

            enhanced.append(enriched)

        self.history.extend(enhanced)
        self.history = self.history[-self.max_history:]

        return enhanced

    # -------------------------
    # 🧠 CATEGORY
    # -------------------------
    def _categorize(self, t):

        t = t.lower()

        if any(x in t for x in ["war","attack","military","missile"]):
            return "geopolitics"

        if any(x in t for x in ["ai","openai","spacex","robot"]):
            return "technology"

        if any(x in t for x in ["bank","ipo","market","billion"]):
            return "economy"

        return "general"

    # -------------------------
    # 🧠 REAL INSIGHT ENGINE
    # -------------------------
    def _extract_insight(self, topic, category):

        t = topic.lower()

        if category == "technology":
            return "accelerating technological power shift"

        if category == "geopolitics":
            return "regional instability escalation"

        if category == "economy":
            return "capital concentration and market expansion"

        return "emerging global signal"

    # -------------------------
    # ⚠️ RISK
    # -------------------------
    def _compute_risk(self, topic, score):

        t = topic.lower()
        risk = score

        if any(x in t for x in ["war","attack","crisis"]):
            risk += 3

        return min(risk, 10)

    # -------------------------
    # 📈 TREND
    # -------------------------
    def _compute_trend(self, topic, score):

        past = [
            h["score"] for h in self.history
            if topic[:30] in h.get("topic", "")
        ]

        if not past:
            return "new"

        avg = sum(past) / len(past)

        if score > avg * 1.3:
            return "surging"
        elif score < avg * 0.7:
            return "declining"

        return "stable"

    # -------------------------
    # 🧠 IMPORTANCE
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
    def _build_summary(self, insight, risk):
        return f"{insight} | risk={risk}"

    def _safe_float(self, x, default=1.0):
        try:
            return float(x)
        except:
            return default

    def _now(self):
        return datetime.utcnow().isoformat()
