class DecisionEngine:

    def evaluate(self, items):

        output = []

        if not isinstance(items, list) or not items:
            return output

        scored = []

        # -------------------------
        # 1. SCORING
        # -------------------------
        for item in items:

            try:
                signal = item.get("signal", {})
                prediction = item.get("prediction", {})
                reasoning = item.get("reasoning", {})

                score = signal.get("score", 0)
                impact = prediction.get("impact_score", 0.5)

                if isinstance(reasoning, dict):
                    confidence = reasoning.get("confidence", 0.5)
                else:
                    confidence = 0.5

                urgency = item.get("urgency", "low")

                urgency_map = {
                    "low": 0.3,
                    "medium": 0.6,
                    "high": 0.9
                }

                urgency_score = urgency_map.get(urgency, 0.3)

                # 🔥 FINAL PRIORITY
                priority = (
                    (score * 0.30) +
                    (impact * 0.25) +
                    (confidence * 0.25) +
                    (urgency_score * 0.20)
                )

                # 🔥 HARD FILTER (KILL)
                if score < 0.2 and impact < 0.3:
                    continue

                scored.append({
                    "item": item,
                    "priority": priority,
                    "meta": {
                        "score": score,
                        "impact": impact,
                        "confidence": confidence,
                        "urgency": urgency
                    }
                })

            except:
                continue

        if not scored:
            return []

        # -------------------------
        # 2. SORT (EN KRİTİK)
        # -------------------------
        scored = sorted(scored, key=lambda x: x["priority"], reverse=True)

        # -------------------------
        # 3. SELECTION LOGIC
        # -------------------------
        TOP_K = 3   # maksimum publish
        MIN_THRESHOLD = 0.45  # taban kalite

        selected = []

        for i, s in enumerate(scored):

            if s["priority"] < MIN_THRESHOLD:
                continue

            if i >= TOP_K:
                break

            selected.append(s)

        # fallback → en az 1 içerik
        if not selected and scored:
            selected = [scored[0]]

        # -------------------------
        # 4. ATTACH DECISION
        # -------------------------
        for s in scored:

            item = s["item"]

            publish = s in selected

            item["decision"] = {
                "publish": publish,
                "priority": round(s["priority"], 3),
                "rank": scored.index(s) + 1,
                **s["meta"]
            }

            output.append(item)

        return output
