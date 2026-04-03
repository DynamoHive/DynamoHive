        enriched.append({
            "topic": s.get("text"),
            "raw_score": score,
            "mentions": mentions,
            "velocity": velocity,
            "spread": spread,
            "sentiment": sentiment,
            "dominance_score": dominance_score
        })

    # normalize
    total = sum([x["dominance_score"] for x in enriched]) or 1

    for x in enriched:
        x["dominance"] = round(x["dominance_score"] / total, 4)

    # sort
    enriched.sort(key=lambda x: x["dominance"], reverse=True)

    return enriched
