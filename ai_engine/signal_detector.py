from collections import defaultdict

def detect_signals(analysis):

    if not analysis:
        print("signals detected: 0")
        return []

    counter = defaultdict(int)

    for item in analysis:

        text = str(item.get("title") or item.get("text") or "").lower()

        if not text:
            continue

        words = [w for w in text.split() if len(w) > 4]

        if len(words) < 3:
            continue

        topic = " ".join(words[:6])
        counter[topic] += 1

    signals = []

    for topic, count in counter.items():

        signals.append({
            "topic": topic,
            "score": float(count),
            "count": count
        })

    # 🔥 KRİTİK: fallback garanti
    if not signals:

        for item in analysis[:10]:

            text = str(item.get("title") or "").lower()

            if not text:
                continue

            signals.append({
                "topic": text[:80],
                "score": 1.0,
                "count": 1
            })

    print("signals detected:", len(signals))

    return signals
