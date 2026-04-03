class GlobalIntelligenceEngine:

    def __init__(self):
        self.history = []
        self.max_history = 300

    # -------------------------
    # MAIN
    # -------------------------
    def process(self, intelligence):

        if not intelligence or not isinstance(intelligence, list):
            return []

        enhanced = []
        seen = set()  # 🔥 duplicate fix

        for item in intelligence:

            if not isinstance(item, dict):
                continue

            topic = str(item.get("topic", "")).strip()
            if len(topic) < 5:
                continue

            key = topic.lower()[:80]
            if key in seen:
                continue
            seen.add(key)

            score = self._safe_float(item.get("score", 1.0))

            category = self._categorize(topic)
            actors = self._extract_actors(topic)
            risk = self._compute_risk(score, topic)
            trend = self._compute_trend(topic, score)

            enriched = {
                "topic": topic,
                "score": round(score, 2),
                "category": category,
                "actors": actors,
                "risk": round(risk, 2),
                "trend": trend,
                "importance": self._importance(score, risk),
                "summary": self._build_summary(topic, category, risk),
                "timestamp": self._now()
            }

            enhanced.append(enriched)

        # 🔥 history safe update
        if enhanced:
            self.history.extend(enhanced)
            self.history = self.history[-self.max_history:]

        return enhanced

    # -------------------------
    # CATEGORY
    # -------------------------
    def _categorize(self, topic):

        t = topic.lower()

        if any(x in t for x in ["war","attack","military","missile","conflict","iran","israel"]):
            return "geopolitics"

        if any(x in t for x in ["ai","technology","robot","openai","spacex","deepmind"]):
            return "technology"

        if any(x in t for x in ["bank","economy","market","billion","ipo","inflation"]):
            return "economy"

        if any(x in t for x in ["election","government","law","court","trump"]):
            return "politics"

        return "general"

    # -------------------------
    # ACTOR EXTRACTION (FIXED)
    # -------------------------
    def _extract_actors(self, topic):

        words = topic.split()

        actors = []

        for w in words:
            w_clean = w.strip(",.()")

            # 🔥 büyük harf + gerçek isim filtresi
            if (
                len(w_clean) > 3
                and w_clean[0].isupper()
                and not w_clean.isupper()  # NASA gibi spam engel
            ):
                actors.append(w_clean)

        return list(dict.fromkeys(actors))[:5]  # unique + order koru

    # -------------------------
    # RISK ENGINE (UPGRADE)
    # -------------------------
    def _compute_risk(self, score, topic):

        t = topic.lower()
        risk = score

        if any(x in t for x in ["war","attack","crisis","explosion","strike"]):
            risk += 3

        if any(x in t for x in ["collapse","bankrupt","failure","crash"]):
            risk += 2

        if any(x in t for x in ["nuclear","missile","drone"]):
            risk += 2

        return min(risk, 10.0)

    # -------------------------
    # TREND (FIXED)
    # -------------------------
    def _compute_trend(self, topic, score):

        if not self.history:
            return "new"

        topic_key = topic.lower()[:40]

        past = [
            h["score"]
            for h in self.history
            if topic_key in h.get("topic", "").lower()
        ]

        if not past:
            return "new"

        avg = sum(past) / len(past)

        if score > avg * 1.4:
            return "surging"
        elif score < avg * 0.7:
            return "declining"
        return "stable"

    # -------------------------
    # IMPORTANCE (FIXED)
    # -------------------------
    def _importance(self, score, risk):

        val = score + risk

        if val >= 12:
            return "critical"
        elif val >= 8:
            return "high"
        elif val >= 5:
            return "medium"
        return "low"

    # -------------------------
    # SUMMARY (UPGRADE)
    # -------------------------
    def _build_summary(self, topic, category, risk):

        return f"[{category.upper()}] {topic} | risk={round(risk,1)}"

    # -------------------------
    def _safe_float(self, x, default=1.0):
        try:
            return float(x)
        except:
            return default

    def _now(self):
        from datetime import datetime
        return datetime.utcnow().isoformat()
