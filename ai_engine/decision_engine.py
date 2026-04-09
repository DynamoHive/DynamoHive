class DecisionEngine:

    def evaluate(self, items):

        output = []

        if not isinstance(items, list):
            return output

        for item in items:

            try:
                signal = item.get("signal", {})
                prediction = item.get("prediction", {})
                reasoning = item.get("reasoning", {})

                score = signal.get("score", 0)
                impact = prediction.get("impact_score", 0.5)

                # güvenli confidence (dict değilse kırılmaz)
                if isinstance(reasoning, dict):
                    confidence = reasoning.get("confidence", 0.5)
                else:
                    confidence = 0.5

                # 🔥 YENİ: URGENCY
                urgency = item.get("urgency", "low")

                urgency_map = {
                    "low": 0.3,
                    "medium": 0.6,
                    "high": 0.9
                }

                urgency_score = urgency_map.get(urgency, 0.3)

                # 🔥 GELİŞMİŞ PRIORITY
                priority = (
                    (score * 0.3) +
                    (impact * 0.25) +
                    (confidence * 0.25) +
                    (urgency_score * 0.2)
                )

                publish = priority > 0.55

                item["decision"] = {
                    "publish": publish,
                    "priority": round(priority, 3),
                    "score": score,
                    "impact": impact,
                    "confidence": confidence,
                    "urgency": urgency
                }

                output.append(item)

            except:
                continue

        return output
