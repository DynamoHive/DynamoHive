def detect_signals(analysis):

    signals = []
    keyword_counter = {}

    # 🔴 0. güvenlik
    if not analysis:
        print("signals detected: 0 (no analysis)")
        return []

    # 🔴 1. keyword frequency (GLOBAL PATTERN)
    for item in analysis:

        if not isinstance(item, dict):
            continue

        text = str(item.get("text", "")).lower()
        keywords = item.get("keywords") or []

        # 🔥 fallback: keywords yoksa text'ten üret
        if not keywords:
            keywords = text.split()[:5]

        for kw in keywords:
            if not kw:
                continue

            kw = str(kw).lower().strip()

            # 🔴 çok kısa / anlamsızları filtrele
            if len(kw) < 3:
                continue

            keyword_counter[kw] = keyword_counter.get(kw, 0) + 1

    # 🔴 2. signal üretimi
    for item in analysis:

        if not isinstance(item, dict):
            continue

        text = str(item.get("text", ""))
        score = item.get("score", 0)

        keywords = item.get("keywords") or []

        # 🔥 fallback again
        if not keywords:
            keywords = text.lower().split()[:5]

        # normalize
        keywords = [
            str(k).lower().strip()
            for k in keywords
            if k and len(str(k).strip()) >= 3
        ]

        keyword_boost = sum(keyword_counter.get(k, 0) for k in keywords)

        # 🔥 GELİŞMİŞ KOŞUL (DAHA AKILLI)
        if (
            score >= 6
            or keyword_boost >= 2
            or (score >= 4 and keyword_boost >= 1)
        ):

            signals.append({
                "text": text,
                "keywords": keywords,
                "score": score,
                "boost": keyword_boost
            })

    print("signals detected:", len(signals))

    return signals
