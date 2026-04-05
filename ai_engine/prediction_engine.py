import math
import time


def predict_trend(intel):

    topic = str(intel.get("topic", "")).lower()
    score = float(intel.get("score", 1.0))
    insight = intel.get("insight", "")

    trend = "neutral"
    risk = "low"
    horizon = "short-term"

    # -------------------------
    # MOMENTUM
    # -------------------------
    if score > 3:
        trend = "rising"
    if score > 6:
        trend = "explosive"

    # -------------------------
    # RISK DETECTION
    # -------------------------
    if any(x in topic for x in ["war", "attack", "missile", "conflict"]):
        risk = "high"
        horizon = "immediate"

    elif any(x in topic for x in ["collapse", "crisis", "default"]):
        risk = "medium"
        horizon = "mid-term"

    elif any(x in topic for x in ["ai", "ipo", "billion", "expansion"]):
        trend = "growth"
        horizon = "mid-term"

    # -------------------------
    # INTELLIGENCE BOOST
    # -------------------------
    if "geopolitical" in insight:
        risk = "high"

    if "ai power shift" in insight:
        trend = "strategic"

    # -------------------------
    # OUTPUT
    # -------------------------
    return {
        "trend": trend,
        "risk": risk,
        "horizon": horizon,
        "confidence": round(math.log1p(score), 2),
        "timestamp": int(time.time())
    }
