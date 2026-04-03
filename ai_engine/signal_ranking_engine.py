import time


def score_signal(signal):

    score = 0

    source = str(signal.get("source", "")).lower()

    if "reuters" in source:
        score += 25
    elif "nyt" in source:
        score += 20
    elif "bbc" in source:
        score += 20
    else:
        score += 10

    text = str(signal.get("text", "")).lower()

    if "war" in text:
        score += 30
    if "ai" in text:
        score += 20
    if "energy" in text:
        score += 20

    timestamp = signal.get("timestamp", 0)

    age = time.time() - float(timestamp)
    hours = age / 3600
    score += max(0, 24 - hours)

    score += signal.get("boost", 0)

    return score


def rank_signals(signals):

    for s in signals:
        s["score"] = score_signal(s)

    return sorted(signals, key=lambda x: x["score"], reverse=True)
