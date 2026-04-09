class ReasoningEngine:

    def analyze(self, signal, context):

        try:
            topic = str(signal.get("topic", "")).lower()

            if any(x in topic for x in ["war", "military", "nato"]):
                insight = "geopolitical"

            elif any(x in topic for x in ["ai", "technology"]):
                insight = "ai power shift"

            elif any(x in topic for x in ["market", "economy"]):
                insight = "economic"

            else:
                insight = "social"

            return {
                "insight": insight,
                "confidence": 0.6
            }

        except:
            return {
                "insight": "general",
                "confidence": 0.5
            }
