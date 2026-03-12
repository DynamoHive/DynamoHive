def rank_signals(signals):

    ranked = []

    for s in signals:

        impact = s.get("impact", 0.5)
        velocity = s.get("velocity", 0.5)
        sources = s.get("sources", 1)
        actors = s.get("actors", 1)

        score = (
            impact * 0.4 +
            velocity * 0.3 +
            min(sources / 5, 1) * 0.2 +
            min(actors / 5, 1) * 0.1
        )

        s["score"] = round(score, 3)

        ranked.append(s)

    ranked.sort(key=lambda x: x["score"], reverse=True)

    return ranked
