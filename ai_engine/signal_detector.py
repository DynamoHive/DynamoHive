from collections import defaultdict
import re


# -------------------------
# CLEAN
# -------------------------
def normalize(text):
    try:
        text = str(text).lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    except:
        return ""


# -------------------------
# MAIN
# -------------------------
def detect_signals(analysis):

    if not analysis:
        print("signals detected: 0")
        return []

    counter = defaultdict(int)
    samples = {}
    seen = set()

    for item in analysis:

        raw = item.get("title") or item.get("text") or ""
        text = normalize(raw)

        if not text:
            continue

        # 🔥 DUPLICATE ENGELLE
        if text in seen:
            continue
        seen.add(text)

        words = [w for w in text.split() if len(w) > 4]

        if len(words) < 3:
            continue

        # 🔥 KRİTİK FIX → PARÇALAMA YOK
        topic = raw.strip()[:120]

        counter[topic] += 1
        samples[topic] = raw

    signals = []

    for topic, count in counter.items():

        signals.append({
            "topic": topic,
            "score": float(count),
            "count": count,
            "samples": [samples.get(topic, topic)]
        })

    # -------------------------
    # 🔥 GARANTİ FALLBACK
    # -------------------------
    if not signals:

        for item in analysis[:10]:

            raw = item.get("title") or item.get("text") or ""
            text = normalize(raw)

            if not text:
                continue

            signals.append({
                "topic": raw[:120],
                "score": 1.0,
                "count": 1,
                "samples": [raw]
            })

    # -------------------------
    # SORT
    # -------------------------
    signals.sort(key=lambda x: x["score"], reverse=True)

    print("signals detected:", len(signals))

    return signals
