def detect_signals(analysis):

    if not analysis or not isinstance(analysis, list):
        print("signals detected: 0")
        return []

    from collections import defaultdict

    keyword_counter = defaultdict(int)
    keyword_scores = defaultdict(float)

    STOPWORDS = {
        "the","and","for","with","that","this","from","are","was","were",
        "has","have","had","but","not","you","your","about","into","over",
        "after","before","between","will","would","could","should"
    }

    def normalize(text):
        try:
            return str(text).lower().strip()
        except:
            return ""

    def safe_float(x, default=0.0):
        try:
            return float(x)
        except:
            return default

    # -------------------------
    # 1. COLLECT (PHRASE MODE)
    # -------------------------
    for item in analysis:

        if not isinstance(item, dict):
            continue

        text = normalize(item.get("text") or item.get("title") or "")
        score = safe_float(item.get("score", 1))

        if not text:
            continue

        words = [
            w for w in text.split()
            if len(w) > 3 and w not in STOPWORDS
        ]

        # 🔥 BIGRAM + TRIGRAM
        phrases = []

        for i in range(len(words) - 1):
            phrases.append(words[i] + " " + words[i+1])

        for i in range(len(words) - 2):
            phrases.append(words[i] + " " + words[i+1] + " " + words[i+2])

        keywords = phrases[:20] if phrases else words[:10]

        for kw in keywords:

            kw = normalize(kw)

            if not kw or len(kw) < 4:
                continue

            keyword_counter[kw] += 1
            keyword_scores[kw] += score

    # -------------------------
    # 2. BUILD (MERGE SIMPLIFIED)
    # -------------------------
    signals = []

    for kw in keyword_counter:

        count = keyword_counter[kw]
        total_score = keyword_scores[kw]

        # 🔥 kritik eşik
        if count < 2:
            continue

        avg_score = total_score / count

        signals.append({
            "topic": kw,
            "keywords": kw.split(),
            "count": count,
            "score": round(avg_score, 2),
            "boost": max(1, count * 2)
        })

    # -------------------------
    # 3. FALLBACK (SİSTEMİ KURTARIR)
    # -------------------------
    if len(signals) <= 2:

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
                "boost": 1
            })

    # -------------------------
    # 4. SORT
    # -------------------------
    signals.sort(
        key=lambda x: (x.get("count", 0), x.get("score", 0)),
        reverse=True
    )

    print("signals detected:", len(signals))

    return signals
