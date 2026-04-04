import re

def enrich_intelligence(signals):

    enriched = []

    for s in signals:

        topic = str(s.get("topic", "")).lower()

        insight = []

        # -------------------------
        # GEOPOLITICAL SIGNALS
        # -------------------------
        if any(x in topic for x in ["war", "attack", "conflict", "missile"]):
            insight.append("geopolitical escalation")

        if any(x in topic for x in ["sanction", "crisis", "collapse"]):
            insight.append("system instability")

        # -------------------------
        # TECH / POWER SIGNALS
        # -------------------------
        if any(x in topic for x in ["ai", "openai", "anthropic", "google"]):
            insight.append("ai power shift")

        if any(x in topic for x in ["ipo", "billion", "valuation"]):
            insight.append("economic expansion")

        # -------------------------
        # SOCIAL SIGNALS
        # -------------------------
        if any(x in topic for x in ["protest", "uprising", "riot"]):
            insight.append("social unrest")

        # -------------------------
        # DEFAULT
        # -------------------------
        if not insight:
            insight.append("emerging pattern")

        enriched.append({
            "topic": s.get("topic"),
            "score": s.get("score", 1.0),
            "insight": ", ".join(insight)
        })

    return enriched
