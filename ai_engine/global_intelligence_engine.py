class GlobalIntelligenceEngine:

    def process(self, intelligence_list):

        if not intelligence_list:
            return []

        enhanced = []

        for intel in intelligence_list:

            topic = intel.get("topic", "unknown")
            summary = intel.get("summary", "")
            trend = intel.get("trend", "emerging")

            # 🔥 BASİT AMA STABİL ANALİZ KATMANI
            enriched = {
                "topic": topic,
                "summary": summary,
                "trend": trend,
                "confidence": self._score_confidence(trend),
                "risk_level": self._estimate_risk(topic),
                "category": self._classify(topic)
            }

            enhanced.append(enriched)

        return enhanced


    def _score_confidence(self, trend):

        if trend == "surging":
            return 0.9
        if trend == "rising":
            return 0.7
        return 0.5


    def _estimate_risk(self, topic):

        topic = topic.lower()

        if any(x in topic for x in ["war", "conflict", "crisis", "attack"]):
            return "high"

        if any(x in topic for x in ["economy", "market", "inflation"]):
            return "medium"

        return "low"


    def _classify(self, topic):

        topic = topic.lower()

        if any(x in topic for x in ["ai", "tech", "robot"]):
            return "technology"

        if any(x in topic for x in ["war", "politics", "government"]):
            return "geopolitics"

        return "general"
