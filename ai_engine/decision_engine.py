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
            # DECISION LOGIC (AYNI)
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


# -------------------------
# FEEDBACK ENGINE
# -------------------------

def update_feedback(items):

    try:
        global PERFORMANCE_LOG

        now = time.time()

        if not isinstance(items, list):
            return

        for i in items:

            if not isinstance(i, dict):
                continue

            decision = i.get("decision")
            trend = i.get("trend_direction", "stable")

            success = 0

            # -------------------------
            # SUCCESS LOGIC
            # -------------------------
            if decision == "push" and trend == "rising":
                success = 1

            elif decision == "ignore" and trend == "weak":
                success = 1

            PERFORMANCE_LOG.append({
                "time": now,
                "decision": decision,
                "success": success
            })

        # log limit
        if len(PERFORMANCE_LOG) > MAX_LOG:
            PERFORMANCE_LOG = PERFORMANCE_LOG[-MAX_LOG:]

    except:
        pass


# -------------------------
# THRESHOLD OPTIMIZER
# -------------------------

def optimize_thresholds():

    try:
        global THRESHOLDS

        if len(PERFORMANCE_LOG) < 20:
            return THRESHOLDS

        success_rate = sum(x.get("success", 0) for x in PERFORMANCE_LOG) / len(PERFORMANCE_LOG)

        # -------------------------
        # ADJUSTMENT LOGIC
        # -------------------------
        if success_rate < 0.4:
            THRESHOLDS["critical"] += 5
            THRESHOLDS["high"] += 3

        elif success_rate > 0.7:
            THRESHOLDS["critical"] -= 2
            THRESHOLDS["high"] -= 1

        # -------------------------
        # BOUNDS
        # -------------------------
        THRESHOLDS["critical"] = max(20, min(100, THRESHOLDS["critical"]))
        THRESHOLDS["high"] = max(10, min(80, THRESHOLDS["high"]))
        THRESHOLDS["medium"] = max(5, min(50, THRESHOLDS["medium"]))

        return THRESHOLDS

    except:
        return THRESHOLDS


# -------------------------
# FULL PIPE (TEK ÇAĞRI)
# -------------------------

def run_decision_pipeline(items):

    try:
        items = make_decisions(items)
        update_feedback(items)
        optimize_thresholds()
        return items

    except:
        return items if isinstance(items, list) else []
