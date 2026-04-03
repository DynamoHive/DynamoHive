def detect_signals(analysis):

    if not analysis or not isinstance(analysis, list):
        print("signals detected: 0")
        return []

    keyword_counter = defaultdict(int)
    keyword_scores = defaultdict(float)
    keyword_texts = defaultdict(list)

    STOPWORDS = {
        "the", "and", "for", "with", "that", "this",
        "from", "are", "was", "were", "has", "have",
        "had", "but", "not", "you", "your", "about"
    }

    # -------------------------
    # 1. COLLECT (🔥 FIXED)
    # -------------------------
    for item in analysis:

        if not isinstance(item, dict):
            continue

        text = normalize(item.get("text") or item.get("title") or "")
        score = safe_float(item.get("score", 1))

        keywords = item.get("keywords") or []

        # 🔥 TEXT → KEYWORD (FILTRELİ)
        if not keywords:
            words = text.split()
            keywords = [
                w for w in words
                if len(w) > 3 and w not in STOPWORDS
            ]

        for kw in keywords:

            kw = normalize(kw)

            if not kw:
                continue

            keyword_counter[kw] += 1
            keyword_scores[kw] += score
            keyword_texts[kw].append(text)

    # -------------------------
    # 2. BUILD SIGNALS (🔥 DAHA AKILLI)
    # -------------------------
    signals = []

    for kw in keyword_counter:

        count = keyword_counter[kw]
        total_score = keyword_scores[kw]

        avg_score = total_score / count if count else 0

        # 🔥 threshold YUMUŞATILDI
        if count < 2 and avg_score < 1:
            continue

        signals.append({
            "topic": kw,
            "keywords": [kw],
            "count": count,
            "score": round(avg_score, 2),
            "boost": max(1, count * 2),
            "samples": keyword_texts[kw][:3]
        })

    # -------------------------
    # 3. FALLBACK (🔥 GÜVENLİ)
    # -------------------------
    if len(signals) <= 1:

        signals = []

        for item in analysis:

            text = normalize(item.get("text") or item.get("title") or "")

            if not text:
                continue

            signals.append({
                "topic": text,
                "keywords": text.split()[:5],
                "count": 1,
                "score": 1.0,
                "boost": 1,
                "samples": [text]
            })

    # -------------------------
    # 4. SORT
    # -------------------------
    try:
        signals.sort(
            key=lambda x: (x.get("count", 0), x.get("score", 0)),
            reverse=True
        )
    except Exception as e:
        print("SIGNAL SORT ERROR:", e)

    print("signals detected:", len(signals))

    return signals
