  ranked.sort(key=lambda x: x.get("score", 0), reverse=True)

    # -------------------------
    # 🔥 SMART MERGE (ASIL FIX)
    # -------------------------
    from difflib import SequenceMatcher

    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio() > 0.75

    merged = []

    for s in ranked:

        topic = normalize(s.get("topic") or s.get("text"))

        if not topic:
            continue

        found = False

        for existing in merged:
            existing_topic = normalize(existing.get("topic") or existing.get("text"))

            if similar(topic, existing_topic):
                # 🔥 aynı topic → birleştir
                existing["score"] += s.get("score", 0)
                existing["count"] = existing.get("count", 1) + 1
                found = True
                break

        if not found:
            merged.append(s)

    # 🔥 FINAL SORT
    merged.sort(key=lambda x: x.get("score", 0), reverse=True)

    return merged
