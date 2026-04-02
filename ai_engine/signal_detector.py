def detect_signals(analysis):

    signals = []
    keyword_counter = {}

    # 🔴 1. keyword frequency hesapla
    for item in analysis:
        keywords = item.get("keywords", [])
        for kw in keywords:
            keyword_counter[kw] = keyword_counter.get(kw, 0) + 1

    # 🔴 2. sinyal üret
    for item in analysis:

        score = item.get("score", 0)
        keywords = item.get("keywords", [])

        # keyword yoğunluğu
        keyword_boost = sum(keyword_counter.get(k, 0) for k in keywords)

        # 🔥 gerçek signal koşulu
        if score > 10 or keyword_boost > 5:

            signals.append({
                "text": item.get("text", ""),
                "keywords": keywords,
                "score": score,
                "boost": keyword_boost
            })

    print("signals detected:", len(signals))

    return signals
