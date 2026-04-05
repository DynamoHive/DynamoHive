import time

# -------------------------
# GLOBAL THRESHOLDS
# -------------------------

THRESHOLDS = {
    "critical": 50,
    "high": 25,
    "medium": 10
}

# performans hafızası
PERFORMANCE_LOG = []

MAX_LOG = 100


# -------------------------
# DECISION ENGINE
# -------------------------

def make_decisions(items):

    try:
        if not isinstance(items, list):
            return []

        output = []

        for i in items:

            if not isinstance(i, dict):
                continue

            score = i.get("importance_score", 0)
            velocity = i.get("event_velocity", 0)
            trend = i.get("trend_direction", "stable")

            action = "ignore"

            # -------------------------
            # DECISION LOGIC
            # -------------------------
            if score >= THRESHOLDS["critical"] and velocity > 0.3:
                action = "push"

            elif score >= THRESHOLDS["high"]:
                action = "monitor"

            elif score >= THRESHOLDS["medium"]:
                action = "watch"

            i["decision"] = action
            output.append(i)

        return output

    except:
        return items if isinstance(items, list) else []
