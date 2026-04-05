import re

# -------------------------
# KEYWORD MAP
# -------------------------

GEO_KEYWORDS = ["war", "attack", "conflict", "missile", "strike"]
CRISIS_KEYWORDS = ["sanction", "crisis", "collapse", "tension"]
AI_KEYWORDS = ["ai", "openai", "anthropic", "google", "model"]
ECON_KEYWORDS = ["ipo", "billion", "valuation", "market", "funding"]
SOCIAL_KEYWORDS = ["protest", "uprising", "riot", "strike"]
TECH_KEYWORDS = ["robot", "automation", "chip", "gpu", "compute"]


# -------------------------
# MAIN
# -------------------------

def enrich_intelligence(signals):

    try:
        if not isinstance(signals, list):
            return []

        enriched = []

        for s in signals:

            if not isinstance(s, dict):
                continue

            topic_raw = str(s.get("topic", "")).strip()

            if not topic_raw:
                continue

            topic = topic_raw.lower()

            insight = []
            score_boost = 0

            # -------------------------
            # GEOPOLITICAL
            # -------------------------
            if any(k in topic for k in GEO_KEYWORDS):
                insight.append("geopolitical escalation")
                score_boost += 2

            if any(k in topic for k in CRISIS_KEYWORDS):
                insight.append("system instability")
                score_boost += 1

            # -------------------------
            # AI / TECH POWER
            # -------------------------
            if any(k in topic for k in AI_KEYWORDS):
                insight.append("ai power shift")
                score_boost += 2

            if any(k in topic for k in TECH_KEYWORDS):
                insight.append("technological acceleration")
                score_boost += 1

            # -------------------------
            # ECONOMIC
            # -------------------------
            if any(k in topic for k in ECON_KEYWORDS):
                insight.append("economic expansion")
                score_boost += 1

            # -------------------------
            # SOCIAL
            # -------------------------
            if any(k in topic for k in SOCIAL_KEYWORDS):
                insight.append("social unrest")
                score_boost += 1

            # -------------------------
            # DEFAULT
            # -------------------------
            if not insight:
                insight.append("emerging pattern")

            # -------------------------
            # BUILD INTEL OBJECT (NO DATA LOSS)
            # -------------------------
            enriched.append({
                **s,  # 🔥 TÜM ESKİ VERİYİ KORUR

                "topic": topic_raw,
                "score": s.get("score", 1.0) + score_boost,
                "insight": ", ".join(insight),

                # 🔥 structured intelligence (ek)
                "information_warfare": {
                    "narratives": insight
                }
            })

        return enriched

    except:
        return signals if isinstance(signals, list) else []
