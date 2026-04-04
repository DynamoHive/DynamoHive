from collections import defaultdict
import re


def normalize(text):
    try:
        text = str(text).lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    except:
        return ""


def compute_score(text, count):

    t = text.lower()
    score = count * 2

    strong = [
        "war","attack","crisis","collapse",
        "ai","nuclear","sanction","conflict"
    ]

    if any(w in t for w in strong):
        score += 3

    return score


def detect_signals(analysis):

    if not analysis:
        print("signals detected: 0")
        return []

    counter = defaultdict(int)
    seen = set()

    for item in analysis:

        raw = item.get("title") or item.get("text") or ""
        text = normalize(raw)

        if not text:
            continue

        if text in seen:
            continue
        seen.add(text)

        topic = raw.strip()[:120]
        counter[topic] += 1

    signals = []

    for topic, count in counter.items():

        score = compute_score(topic, count)

        signals.append({
            "topic": topic,
            "score": score,
            "count": count
        })

    if not signals:
        for item in analysis[:10]:
            raw = item.get("title") or ""
            if raw:
                signals.append({
                    "topic": raw[:120],
                    "score": 1.0,
                    "count": 1
                })

    signals.sort(key=lambda x: x["score"], reverse=True)

    print("signals detected:", len(signals))

    return signals
