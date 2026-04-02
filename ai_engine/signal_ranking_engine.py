import time


def score_signal(signal):

    score = 0

    # 🔴 1. SOURCE (safe)
    source = str(signal.get("source", "")).lower()

    if "reuters" in source:
        score += 25
    elif "nyt" in source or "new york times" in source:
        score += 20
    elif "bbc" in source:
        score += 20
    else:
        score += 10

    # 🔴 2. KEYWORDS (SENİN SİSTEME UYUMLU)
    keywords = signal.get("keywords") or []
    text = str(signal.get("text", "")).lower()

    KEYWORD_WEIGHTS = {
        "war": 30,
        "conflict": 25,
        "sanction": 20,
        "ai": 20,
        "chip": 20,
        "energy": 20,
        "oil": 20,
        "inflation": 15,
        "supply": 10,
        "chain": 10
    }

    # keyword varsa onu kullan
    for kw in keywords:
        kw = str(kw).lower()
        if kw in KEYWORD_WEIGHTS:
            score += KEYWORD_WEIGHTS[kw]

    # fallback: text içinde ara
    for k, w in KEYWORD_WEIGHTS.items():
        if k in text:
            score += w

    # 🔴 3. FRESHNESS (safe)
    timestamp = signal.get("timestamp")

    if timestamp:
        try:
            age = time.time() - float(timestamp)
            hours = age / 3600
            freshness = max(0, 24 - hours)
            score += freshness
        except:
            pass

    # 🔴 4. LENGTH (safe)
    content = str(signal.get("content", ""))

    score += min(len(content) / 50, 10)

    # 🔴 5. BOOST (senin signal engine’den geliyor)
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
