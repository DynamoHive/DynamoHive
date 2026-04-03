import time
from collections import defaultdict


WINDOW = 3600  # 1 saat


def safe_float(x, default=0.0):
    try:
        return float(x)
    except:
        return default


def normalize(text):
    try:
        return str(text).lower().strip()
    except:
        return ""


def detect_signals(analysis):

    if not analysis or not isinstance(analysis, list):
        print("signals detected: 0")
        return []

    keyword_counter = defaultdict(int)
    keyword_scores = defaultdict(float)
    keyword_texts = defaultdict(list)

    # -------------------------
    # 1. COLLECT
    # -------------------------
    for item in analysis:

        if not isinstance(item, dict):
            continue

        keywords = item.get("keywords") or []

        if not keywords and item.get("topic"):
            keywords = [item.get("topic")]

        text = normalize(item.get("text", ""))
        score = safe_float(item.get("score", 0))

        for kw in keywords:

            kw = normalize(kw)

            if not kw or len(kw) < 3:
                continue

            keyword_counter[kw] += 1
            keyword_scores[kw] += score
            keyword_texts[kw].append(text)

    # -------------------------
    # 2. BUILD SIGNALS (CLEAN)
    # -------------------------
    signals = []

    for kw in keyword_counter:

        count = keyword_counter[kw]
        total_score = keyword_scores[kw]

        avg_score = total_score / count if count else 0

        signals.append({
            # 🔥 ARTIK TEXT YOK (kirlenmeyi engeller)
            "topic": kw,
            "keywords": [kw],
            "count": count,
            "score": round(avg_score, 2),
            "boost": max(1, count * 2),
            "samples": keyword_texts[kw][:3]
        })

    # -------------------------
    # 3. FALLBACK (SAFE)
    # -------------------------
    if not signals:

        for item in analysis:
            text = normalize(item.get("text", ""))

            if text:
                signals.append({
                    "topic": text[:30],
                    "keywords": [text[:10]],
                    "count": 1,
                    "score": 1,
                    "boost": 1,
                    "samples": [text]
                })
                break

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
