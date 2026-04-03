def rank_signals(signals):

    if not signals or not isinstance(signals, list):
        return []

    # 🔥 BOOST MAP
    try:
        boost_map = get_topic_boost()
        if not isinstance(boost_map, dict):
            boost_map = {}
    except Exception as e:
        print("BOOST ERROR:", e)
        boost_map = {}

    # 🔥 BASE SCORE
    base_scored = []

    for s in signals:

        if not isinstance(s, dict):
            continue

        try:
            s["score"] = score_signal(s, boost_map, {})
            base_scored.append(s)
        except Exception as e:
            print("BASE SCORE ERROR:", e)

    # 🔥 INTELLIGENCE
    intelligence = build_intelligence(base_scored)

    # 🔥 FINAL SCORE
    ranked = []

    for s in base_scored:
        try:
            s["score"] = score_signal(s, boost_map, intelligence)
            ranked.append(s)
        except Exception as e:
            print("FINAL SCORE ERROR:", e)

    # 🔥 SORT
    ranked.sort(key=lambda x: x.get("score", 0), reverse=True)

    # -------------------------
    # 🔥 CRITICAL FIX → MERGE DUPLICATES
    # -------------------------
    merged = {}

    for s in ranked:

        topic = normalize(s.get("topic") or s.get("text"))

        if not topic:
            continue

        if topic not in merged:
            merged[topic] = s
        else:
            # score birleştir
            merged[topic]["score"] += s.get("score", 0)

            # count artır
            merged[topic]["count"] = merged[topic].get("count", 1) + 1

    final = list(merged.values())

    # tekrar sırala
    final.sort(key=lambda x: x.get("score", 0), reverse=True)

    return final
