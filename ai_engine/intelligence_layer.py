def enrich_intelligence(signals):

    enriched = []

    for s in signals:

        topic = s.get("topic", "")
        base = float(s.get("score", 1.0))

        narratives = []
        actors = []

        t = topic.lower()

        if "war" in t or "attack" in t:
            narratives.append("conflict")

        if "ai" in t or "openai" in t:
            narratives.append("ai dominance")

        for a in ["usa","china","russia","iran","israel","openai","google","tesla"]:
            if a in t:
                actors.append(a)

        score = base + len(narratives)*1.5 + len(actors)*1.2

        enriched.append({
            "topic": topic,
            "score": round(score,2),
            "information_warfare": {"narratives": narratives},
            "power": {"actors": actors},
            "insight": topic
        })

    return enriched
