def enrich_intelligence(signals):

    if not isinstance(signals, list):
        return []

    enriched = []

    for s in signals:

        if not isinstance(s, dict):
            continue

        topic = str(s.get("topic", "")).strip()
        if not topic:
            continue

        score = s.get("score", 1.0)

        try:
            score = float(score)
        except:
            score = 1.0

        topic_lower = topic.lower()

        insight = []
        boost = 0.0

        # GEO
        if any(k in topic_lower for k in ["war", "attack", "missile", "strike"]):
            insight.append("geopolitical escalation")
            boost += 2.0

        # CRISIS
        if any(k in topic_lower for k in ["crisis", "collapse", "sanction"]):
            insight.append("system instability")
            boost += 1.0

        # AI
        if any(k in topic_lower for k in ["ai", "model", "openai", "google"]):
            insight.append("ai power shift")
            boost += 2.0

        # TECH
        if any(k in topic_lower for k in ["chip", "gpu", "robot", "automation"]):
            insight.append("technological acceleration")
            boost += 1.0

        # ECON
        if any(k in topic_lower for k in ["market", "ipo", "valuation", "funding"]):
            insight.append("economic expansion")
            boost += 1.0

        # SOCIAL
        if any(k in topic_lower for k in ["protest", "riot", "strike"]):
            insight.append("social unrest")
            boost += 1.0

        if not insight:
            insight.append("emerging pattern")

        enriched.append({
            **s,
            "topic": topic,
            "score": round(score + boost, 3),
            "insight": ", ".join(insight)
        })

    return enriched
