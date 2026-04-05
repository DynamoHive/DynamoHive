def compute_importance(items):

    try:
        if not isinstance(items, list):
            return []

        out = []

        for i in items:

            if not isinstance(i, dict):
                continue

            score = i.get("score", 0)
            count = i.get("count", 1)
            velocity = i.get("event_velocity", 0)
            trend = i.get("trend_direction", "stable")
            insight = i.get("insight", "")

            importance = score

            # -------------------------
            # FREQUENCY BOOST
            # -------------------------
            if count > 1:
                importance += count * 2

            # -------------------------
            # EVENT VELOCITY
            # -------------------------
            if velocity > 0.2:
                importance += 5

            # -------------------------
            # TREND
            # -------------------------
            if trend == "rising":
                importance += 3

            # -------------------------
            # DOMAIN WEIGHT
            # -------------------------
            if "geopolitical" in insight:
                importance += 5

            if "ai" in insight:
                importance += 4

            if "economic" in insight:
                importance += 3

            # -------------------------
            # LEVEL
            # -------------------------
            if importance >= 25:
                level = "critical"
            elif importance >= 15:
                level = "high"
            elif importance >= 8:
                level = "medium"
            else:
                level = "low"

            i["importance_score"] = importance
            i["importance_level"] = level

            # 🔥 DOMINANCE FLAG
            i["dominant"] = True if importance >= 20 else False

            out.append(i)

        return out

    except:
        return items if isinstance(items, list) else []
