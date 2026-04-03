import time
from backend.analytics_engine import get_topic_boost


# -------------------------
# SAFE HELPERS
# -------------------------

def safe_str(x):
    try:
        return str(x)
    except:
        return ""


def safe_float(x, default=0.0):
    try:
        return float(x)
    except:
        return default


def normalize(text):
    return safe_str(text).lower()


# -------------------------
# CORE SCORING BLOCKS
# -------------------------

def source_score(source):

    source = normalize(source)

    if "reuters" in source:
        return 25
    elif "nyt" in source or "new york times" in source:
        return 20
    elif "bbc" in source:
        return 20
    else:
        return 10


def keyword_score(text):

    score = 0

    if "war" in text:
        score += 30
    if "ai" in text:
        score += 20
    if "energy" in text:
        score += 20

    return score


def freshness_score(timestamp):

    try:
        age = time.time() - safe_float(timestamp)
        hours = age / 3600
        return max(0, 24 - hours)
    except:
        return 0


def event_boost_score(text, boost_map):

    if not boost_map or not isinstance(boost_map, dict):
        return 0

    total = 0

    for topic, boost in boost_map.items():

        topic = normalize(topic)
        boost = safe_float(boost)

        if not topic or boost <= 0:
            continue

        words = topic.split()

        if not words:
            continue

        match_count = 0

        for w in words:
            if w in text:
                match_count += 1

        if match_count > 0:
            ratio = match_count / len(words)

            # 🔥 AGGRESSIVE + SAFE BOOST
            total += boost * ratio * 2.5

    return total


# -------------------------
# MAIN SCORING
# -------------------------

def score_signal(signal, boost_map):

    try:
        text = normalize(signal.get("text", ""))
        source = signal.get("source", "")
        timestamp = signal.get("timestamp", 0)

        score = 0

        score += source_score(source)
        score += keyword_score(text)
        score += freshness_score(timestamp)

        # 🔥 EVENT INTELLIGENCE
        score += event_boost_score(text, boost_map)

        return round(score, 2)

    except Exception as e:
        print("SCORE ERROR:", e)
        return 0


# -------------------------
# RANKING ENGINE
# -------------------------

def rank_signals(signals):

    if not signals or not isinstance(signals, list):
        return []

    # 🔥 BOOST SAFE LOAD
    try:
        boost_map = get_topic_boost()
        if not isinstance(boost_map, dict):
            boost_map = {}
    except Exception as e:
        print("BOOST ERROR:", e)
        boost_map = {}

    ranked = []

    for s in signals:

        if not isinstance(s, dict):
            continue

        try:
            s["score"] = score_signal(s, boost_map)
            ranked.append(s)
        except Exception as e:
            print("RANK ITEM ERROR:", e)

    try:
        ranked.sort(key=lambda x: x.get("score", 0), reverse=True)
    except Exception as e:
        print("SORT ERROR:", e)

    return ranked
