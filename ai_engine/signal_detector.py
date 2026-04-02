import time
from collections import defaultdict


WINDOW = 3600        # 1 saat
MIN_COUNT = 3        # minimum tekrar
MIN_SCORE = 5        # minimum analiz skoru


def detect_signals(analysis):

    if not analysis:
        print("signals detected: 0")
        return []

    keyword_counter = defaultdict(int)
    keyword_scores = defaultdict(float)
    keyword_texts = defaultdict(list)

    # -------------------------
    # 1. TOPLA (GERÇEK AGGREGATION)
    # -------------------------
    for item in analysis:

        if not isinstance(item, dict):
            continue

        keywords = item.get("keywords") or []

        if not keywords and item.get("topic"):
            keywords = [item.get("topic")]

        score = float(item.get("score", 0))
        text = item.get("text", "")

        for kw in keywords:
            kw = str(kw).lower().strip()

            if not kw:
                continue

            keyword_counter[kw] += 1
            keyword_scores[kw] += score
            keyword_texts[kw].append(text)

    # -------------------------
    # 2. SIGNAL ÜRET
    # -------------------------
    signals = []

    for kw in keyword_counter:

        count = keyword_counter[kw]
        total_score = keyword_scores[kw]

        avg_score = total_score / count if count else 0

        # 🔥 GERÇEK FİLTRE
        if count >= MIN_COUNT or avg_score >= MIN_SCORE:

            signals.append({
                "text": kw,
                "keywords": [kw],
                "count": count,
                "score": round(avg_score, 2),
                "boost": count,
                "samples": keyword_texts[kw][:3]
            })

    print("signals detected:", len(signals))

    return signals
