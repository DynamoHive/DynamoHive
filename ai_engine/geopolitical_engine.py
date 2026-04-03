# ai_engine/geopolitical_engine.py

KEYWORD_MAP = {
    "iran": "middle_east",
    "israel": "middle_east",
    "gaza": "middle_east",
    "ukraine": "europe",
    "russia": "europe",
    "china": "asia",
    "taiwan": "asia",
    "usa": "america",
    "trump": "america",
    "eu": "europe"
}


def map_region(topic):

    topic = str(topic).lower()

    for k, region in KEYWORD_MAP.items():
        if k in topic:
            return region

    return "global"


def build_geopolitical_map(signals):

    regions = {}

    for s in signals:

        topic = s.get("text") or "unknown"
        score = s.get("score", 0)

        region = map_region(topic)

        regions[region] = regions.get(region, 0) + score

    result = []

    total = sum(regions.values()) or 1

    for r, val in regions.items():
        result.append({
            "region": r,
            "score": val,
            "ratio": round(val / total, 3)
        })

    result.sort(key=lambda x: x["score"], reverse=True)

    return result
