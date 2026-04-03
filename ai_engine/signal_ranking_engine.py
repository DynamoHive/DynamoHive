  content = str(signal.get("content", ""))
    score += min(len(content) / 50, 10)

    # BOOST (event sonrası)
    score += signal.get("boost", 0)

    return round(score, 2)


def rank_signals(signals):

    if not signals:
        return []

    ranked = []

    for s in signals:
        if not isinstance(s, dict):
            continue

        s["score"] = score_signal(s)
        ranked.append(s)

    ranked.sort(key=lambda x: x["score"], reverse=True)

    print("top signal:", ranked[0] if ranked else None)

    return ranked
