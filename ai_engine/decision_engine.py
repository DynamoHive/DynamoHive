class DecisionEngine:

    def evaluate(self, items):

        if not isinstance(items, list) or not items:
            return []

        scored = []

        # =====================================================
        # 1. SAFE NORMALIZATION
        # =====================================================
        def normalize(item):
            if not isinstance(item, dict):
                return {}

            return {
                "topic": item.get("topic") or item.get("title") or "unknown",
                "score": item.get("score", 0.5),
                "impact": item.get("impact", 0.5),
                "urgency": item.get("urgency", "medium"),
                "raw": item
            }

        # =====================================================
        # 2. SCORING
        # =====================================================
        for item in items:

            try:
                n = normalize(item)

                score = float(n["score"])
                impact = float(n["impact"])

                urgency_map = {
                    "low": 0.3,
                    "medium": 0.6,
                    "high": 0.9
                }

                urgency_score = urgency_map.get(n["urgency"], 0.6)

                confidence = 0.5  # default safe

                priority = (
                    (score * 0.40) +
                    (impact * 0.30) +
                    (confidence * 0.10) +
                    (urgency_score * 0.20)
                )

                # relaxed filter (CRITICAL FIX)
                if score < 0.05 and impact < 0.1:
                    continue

                scored.append({
                    "item": n,
                    "priority": priority,
                    "meta": {
                        "score": score,
                        "impact": impact,
                        "confidence": confidence,
                        "urgency": n["urgency"]
                    }
                })

            except Exception:
                continue

        # =====================================================
        # 3. FALLBACK (NO EMPTY OUTPUT GUARANTEE)
        # =====================================================
        if not scored:
            return [
                {
                    "item": {
                        "topic": i.get("topic", "fallback"),
                        "score": i.get("score", 0.5)
                    },
                    "priority": 0.5,
                    "decision": {
                        "publish": True,
                        "priority": 0.5,
                        "rank": idx + 1
                    }
                }
                for idx, i in enumerate(items[:10])
            ]

        # =====================================================
        # 4. SORT
        # =====================================================
        scored.sort(key=lambda x: x["priority"], reverse=True)

        # =====================================================
        # 5. SELECT TOP
        # =====================================================
        TOP_K = 5
        MIN_THRESHOLD = 0.2

        selected = []
        used_topics = set()

        for s in scored:

            if len(selected) >= TOP_K:
                break

            if s["priority"] < MIN_THRESHOLD:
                continue

            topic = str(s["item"]["topic"]).lower()

            if topic in used_topics:
                continue

            used_topics.add(topic)
            selected.append(s)

        selected_set = set(id(x["item"]) for x in selected)

        # =====================================================
        # 6. ATTACH DECISION
        # =====================================================
        output = []

        for idx, s in enumerate(scored):

            item = s["item"]
            is_selected = id(item) in selected_set

            item["decision"] = {
                "publish": is_selected,
                "priority": round(s["priority"], 3),
                "rank": idx + 1,
                **s["meta"]
            }

            output.append(item)

        return output
