import math
import time


def predict_trend(intel):

    topic = str(intel.get("topic", "")).lower()
    score = float(intel.get("score", 1.0))
    insight = str(intel.get("insight", ""))

    trend = "neutral"
    risk = "low"
    horizon = "short-term"

    if score > 3:
        trend = "rising"
    if score > 6:
        trend = "explosive"

    if any(x in topic for x in ["war", "attack", "missile", "conflict"]):
        risk = "high"
        horizon = "immediate"

    elif any(x in topic for x in ["collapse", "crisis", "default"]):
        risk = "medium"
        horizon = "mid-term"

    elif any(x in topic for x in ["ai", "ipo", "billion", "expansion"]):
        trend = "growth"
        horizon = "mid-term"

    if "geopolitical" in insight:
        risk = "high"

    if "ai power shift" in insight:
        trend = "strategic"

    return {
        "trend": trend,
        "risk": risk,
        "horizon": horizon,
        "confidence": round(math.log1p(score), 2),
        "timestamp": int(time.time())
    }


class PredictionEngine:

    def forecast(self, signal, context):

        try:
            # 🔥 DOĞRU ŞEKİL (dict içinde assignment YOK)
            topic = signal.get("topic") or signal.get("title") or ""

            intel = {
                "topic": topic,
                "score": signal.get("score", 1.0),
                "insight": context.get("insight", "")
            }

            result = predict_trend(intel)

            result["impact_score"] = result.get("confidence", 0.5)

            risk = result.get("risk", "low")
            urgency_map = {
                "low": "low",
                "medium": "medium",
                "high": "high"
            }

            result["urgency"] = urgency_map.get(risk, "low")

            return result

        except Exception as e:
            print("PREDICTION ERROR:", e)

            return {
                "trend": "neutral",
                "risk": "low",
                "horizon": "short-term",
                "confidence": 0.5,
                "impact_score": 0.5,
                "urgency": "low"
            }
