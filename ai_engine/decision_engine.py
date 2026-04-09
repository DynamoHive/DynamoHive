class DecisionEngine:

    def evaluate(self, items):

        output = []

        for item in items:

            score = item.get("signal", {}).get("score", 0)

            impact = item.get("prediction", {}).get("impact_score", 0.5)
            confidence = item.get("reasoning", {}).get("confidence", 0.5)

            priority = (score * 0.4) + (impact * 0.3) + (confidence * 0.3)

            publish = priority > 0.6

            item["decision"] = {
                "publish": publish,
                "priority": priority
            }
