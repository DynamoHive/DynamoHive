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

    # 🔥 EVENT BOOST (ANA NOKTA)
    for topic, boost in boost_map.items():
        if topic and topic in text:
            score += boost

    # 🔴 FRESHNESS
    timestamp = signal.get("timestamp", 0)

    try:
        age = time.time() - float(timestamp)
        hours = age / 3600
        score += max(0, 24 - hours)
    except:
        pass

    return score


def rank_signals(signals):

    if not signals:
        return []

    # 🔥 analytics bağlantısı
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
