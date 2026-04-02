def detect_signals(analysis):

    signals = []
    keyword_counter = {}

    # 🔴 0. güvenlik
    if not analysis:
        print("signals detected: 0 (no analysis)")
        return []

    # 🔴 1. keyword frequency
    for item in analysis:
        if not isinstance(item, dict):
            continue

        keywords = item.get("keywords") or []
        
        # fallback: keywords yoksa topic kullan
        if not keywords and item.get("topic"):
            keywords = [item.get("topic")]

        for kw in keywords:
            if kw:
                kw = str(kw).lower().strip()
                keyword_counter[kw] = keyword_counter.get(kw, 0) + 1

    # 🔴 2. signal üret
    for item in analysis:

        if not isinstance(item, dict):
            continue

        score = item.get("score", 0)
        keywords = item.get("keywords") or []

        # fallback again
        if not keywords and item.get("topic"):
            keywords = [item.get("topic")]

        # normalize
        keywords = [str(k).lower().strip() for k in keywords if k]

        keyword_boost = sum(keyword_counter.get(k, 0) for k in keywords)

        # 🔥 daha dengeli threshold
        if score > 8 or keyword_boost > 3:

            signals.append({
                "text": item.get("text", ""),
                "keywords": keywords,
                "score": score,
                "boost": keyword_boost
            })

    print("signals detected:", len(signals))

    return signals
