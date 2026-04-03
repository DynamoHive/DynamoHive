def compute_dominance(signals):

    if not signals:
        return []

    ranked = sorted(
        signals,
        key=lambda x: x.get("score", 0),
        reverse=True
    )

    result = []

    for i, s in enumerate(ranked[:10]):

        result.append({
            "topic": s.get("topic"),
            "score": s.get("score"),
            "rank": i + 1
        })

    return result
