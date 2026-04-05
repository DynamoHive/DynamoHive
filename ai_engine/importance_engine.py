# -------------------------
# IMPORTANCE ENGINE
# -------------------------

def compute_importance(signals):

    try:
        if not isinstance(signals, list):
            return []

        output = []

        for s in signals:

            if not isinstance(s, dict):
                continue

            base_score = s.get("score", 0)
            event_count = s.get("event_count", 0)
            velocity = s.get("event_velocity", 0)
            trend_score = s.get("trend_score", 0)

            # -------------------------
            # FINAL IMPORTANCE SCORE
            # -------------------------
            importance = (
                base_score +
                (event_count * 2) +
                (velocity * 10) +
                trend_score
            )

            # -------------------------
            # LEVEL
            # -------------------------
            level = "low"

            if importance >= 50:
                level = "critical"
            elif importance >= 25:
                level = "high"
            elif importance >= 10:
                level = "medium"

            # -------------------------
            # DOMINANCE
            # -------------------------
            dominance = False

            if level == "critical" and velocity > 0.3:
                dominance = True

            # -------------------------
            # UPDATE OBJECT
            # -------------------------
            s["importance_score"] = round(importance, 2)
            s["importance_level"] = level
            s["dominant"] = dominance

            output.append(s)

        # -------------------------
        # SORT
        # -------------------------
        output.sort(key=lambda x: x.get("importance_score", 0), reverse=True)

        return output

    except:
        return signals if isinstance(signals, list) else []
