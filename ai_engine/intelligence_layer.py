from collections import defaultdict


def normalize(x):
    try:
        return str(x).lower()
    except:
        return ""


def build_intelligence(signals):

    if not signals:
        return {}

    topic_strength = defaultdict(float)
    topic_count = defaultdict(int)

    # -------------------------
    # 1. TOPLA
    # -------------------------
    for s in signals:

        topic = normalize(s.get("topic") or s.get("text"))
        score = float(s.get("score", 0))
        count = int(s.get("count", 1))

        topic_strength[topic] += score * count
        topic_count[topic] += count

    # -------------------------
    # 2. DOMINANCE
    # -------------------------
    intelligence = {}

    total = sum(topic_strength.values()) or 1

    for topic in topic_strength:

        strength = topic_strength[topic]
        count = topic_count[topic]

        dominance = strength / total

        intelligence[topic] = {
            "strength": round(strength, 2),
            "count": count,
            "dominance": round(dominance, 4)
        }

    return intelligence
