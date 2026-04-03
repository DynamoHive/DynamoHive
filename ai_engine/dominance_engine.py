# ai_engine/dominance_engine.py

def compute_dominance(signals):

    if not signals:
        return []

    enriched = []

    for s in signals:
        score = s.get("score", 0)
        mentions = s.get("mentions", 1)
        velocity = s.get("velocity", 0)
        sentiment = s.get("sentiment", 0)
        sources = s.get("sources", [])

        freq = mentions
        spread = len(set(sources))
        sentiment_impact = abs(sentiment)

        dominance_score = (
            score * 0.3 +
            freq * 0.2 +
            velocity * 0.2 +
            spread * 0.2 +
            sentiment_impact * 0.1
        )

        enriched.append({
            "topic": s.get("text"),
            "raw_score": score,
            "mentions": mentions,
            "velocity": velocity,
            "spread": spread,
            "sentiment": sentiment,
            "dominance_score": dominance_score
        })

    total = sum(x["dominance_score"] for x in enriched) or 1

    for x in enriched:
        x["dominance"] = round(x["dominance_score"] / total, 4)

    enriched.sort(key=lambda x: x["dominance"], reverse=True)

    return enriched
