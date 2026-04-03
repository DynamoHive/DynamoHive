import time
from backend.analytics_engine import get_topic_boost


def score_signal(signal, boost_map):

    score = 0

    # 🔴 SOURCE
    source = str(signal.get("source", "")).lower()

    if "reuters" in source:
        score += 25
    elif "nyt" in source or "new york times" in source:
        score += 20
    elif "bbc" in source:
        score += 20
    else:
        score += 10

    # 🔴 TEXT
    text = str(signal.get("text", "")).lower()

    if "war" in text:
        score += 30
    if "ai" in text:
        score += 20
    if "energy" in text:
        score += 20

    # 🔥 STRONG EVENT MATCHING
    for topic, boost in boost_map.items():

        if not topic:
            continue

        topic_words = topic.split()
        if not topic_words:
            continue

        match_count = 0

        for w in topic_words:
            if w in text:
                match_count += 1

        if match_count > 0:
            # 🔥 agresif boost (ANA FARK)
            ratio = match_count / len(topic_words)
            score += boost * ratio * 2   # <-- güçlendirilmiş

    # 🔴 FRESHNESS
    timestamp = signal.get("timestamp", 0)

    try:
        age = time.time() - float(timestamp)
        hours = age / 3600

        freshness = max(0, 24 - hours)

        score += freshness
    except:
        pass

    return round(score, 2)


def rank_signals(signals):

    if not signals:
        return []

    boost_map = get_topic_boost()

    ranked = []

    for s in signals:

        if not isinstance(s, dict):
            continue

        try:
            s["score"] = score_signal(s, boost_map)
            ranked.append(s)
        except Exception as e:
            print("RANK ERROR:", e)

    ranked.sort(key=lambda x: x.get("score", 0), reverse=True)

    return ranked
