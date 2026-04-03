import re

# -------------------------
# 🔥 KNOWN ACTORS
# -------------------------

COUNTRIES = [
    "usa", "china", "russia", "iran", "israel",
    "france", "germany", "uk", "turkey"
]

COMPANIES = [
    "openai", "google", "microsoft", "spacex",
    "tesla", "anthropic", "meta", "amazon"
]

# -------------------------
# 🔥 MAIN
# -------------------------

def map_power(intel):

    topic = str(intel.get("topic", "")).lower()
    insight = str(intel.get("insight", "")).lower()

    actors = extract_actors(topic)

    winners = []
    losers = []

    for a in actors:

        score = evaluate_actor(a, topic, insight)

        if score > 0:
            winners.append((a, score))
        elif score < 0:
            losers.append((a, score))

    winners.sort(key=lambda x: x[1], reverse=True)
    losers.sort(key=lambda x: x[1])

    return {
        "actors": actors,
        "winners": [a for a, _ in winners[:3]],
        "losers": [a for a, _ in losers[:3]],
        "dominant": winners[0][0] if winners else None
    }


# -------------------------
# 🔍 ACTOR EXTRACTION
# -------------------------

def extract_actors(text):

    actors = []

    for c in COUNTRIES:
        if c in text:
            actors.append(c)

    for c in COMPANIES:
        if c in text:
            actors.append(c)

    return list(set(actors))


# -------------------------
# ⚖️ POWER LOGIC
# -------------------------

def evaluate_actor(actor, topic, insight):

    score = 0

    # 🔥 POSITIVE SIGNALS
    if any(x in topic for x in ["launch", "growth", "expansion", "ipo", "billion"]):
        score += 2

    if any(x in insight for x in ["power shift", "expansion", "dominance"]):
        score += 2

    # 🔥 NEGATIVE SIGNALS
    if any(x in topic for x in ["attack", "crisis", "collapse", "sanction"]):
        score -= 2

    if any(x in insight for x in ["instability", "risk"]):
        score -= 1

    return score
