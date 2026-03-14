import math
import time


def score_signal(signal):

    score = 0

    # 1️⃣ kaynak güvenilirliği
    source = signal.get("source", "")

    if "reuters" in source:
        score += 25
    elif "nyt" in source:
        score += 20
    elif "bbc" in source:
        score += 20
    else:
        score += 10

    # 2️⃣ anahtar kelime ağırlığı
    title = signal.get("title", "").lower()

    KEYWORD_WEIGHTS = {
        "war": 30,
        "conflict": 25,
        "sanction": 20,
        "ai": 20,
        "chip": 20,
        "energy": 20,
        "oil": 20,
        "inflation": 15,
        "supply chain": 20
    }

    for k, w in KEYWORD_WEIGHTS.items():
        if k in title:
            score += w

    # 3️⃣ zaman faktörü
    timestamp = signal.get("timestamp")

    if timestamp:

        age = time.time() - timestamp

        hours = age / 3600

        freshness = max(0, 24 - hours)

        score += freshness

    # 4️⃣ uzunluk faktörü
    content = signal.get("content", "")

    score += min(len(content) / 50, 10)

    return round(score, 2)


def rank_signals(signals):

    ranked = []

    for s in signals:

        s["score"] = score_signal(s)

        ranked.append(s)

    ranked.sort(key=lambda x: x["score"], reverse=True)

    return ranked
