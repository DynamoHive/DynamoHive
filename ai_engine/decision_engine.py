class DecisionEngine:

    def evaluate(self, items):

        if not isinstance(items, list) or not items:
            return []

        scored = []

        def normalize(item):
            if not isinstance(item, dict):
                return {}

            return {
                "topic": item.get("topic") or item.get("title") or "unknown",
                "score": float(item.get("score", 0.5)),
                "impact": float(item.get("impact", 0.5)),
                "urgency": item.get("urgency", "medium"),
                "raw": item
            }

        # -------------------------
        # SCORING
        # -------------------------
        for item in items:

            try:
                n = normalize(item)

                urgency_map = {
                    "low": 0.3,
                    "medium": 0.6,
                    "high": 0.9
                }

                urgency_score = urgency_map.get(n["urgency"], 0.6)
                confidence = 0.55  # slightly increased stability

                priority = (
                    (n["score"] * 0.40) +
                    (n["impact"] * 0.30) +
                    (confidence * 0.10) +
                    (urgency_score * 0.20)
                )

                if n["score"] < 0.05 and n["impact"] < 0.1:
                    continue

                scored.append({
                    "item": n,
                    "priority": priority,
                    "meta": {
                        "score": n["score"],
                        "impact": n["impact"],
                        "confidence": confidence,
                        "urgency": n["urgency"]
                    }
                })

            except Exception:
                continue

        # -------------------------
        # HARD FALLBACK FIX (IMPORTANT)
        # -------------------------
        if not scored:
            return [
                {
                    "topic": i.get("topic", "fallback"),
                    "score": i.get("score", 0.5),
                    "decision": {
                        "publish": True,
                        "priority": 0.5,
                        "rank": idx + 1,
                        "score": i.get("score", 0.5),
                        "impact": 0.5,
                        "confidence": 0.5,
                        "urgency": "medium"
                    }
                }
                for idx, i in enumerate(items[:10])
            ]

        # -------------------------
        # SORT
        # -------------------------
        scored.sort(key=lambda x: x["priority"], reverse=True)

        # -------------------------
        # SELECT TOP
        # -------------------------
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

        # 🔥 FIX: no id() dependency anymore
        selected_topics = set(str(x["item"]["topic"]).lower() for x in selected)

        # -------------------------
        # ATTACH DECISION
        # -------------------------
        output = []

        for idx, s in enumerate(scored):

            item = s["item"]
            topic = str(item["topic"]).lower()

            is_selected = topic in selected_topics

            item["decision"] = {
                "publish": is_selected,
                "priority": round(s["priority"], 3),
                "rank": idx + 1,
                **s["meta"]
            }

            output.append(item)

        return output
