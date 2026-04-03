# ai_engine/geopolitical_engine.py

from ai_engine.geopolitical_signals import detect_geopolitical_signal


# -------------------------
# REGION MAP
# -------------------------
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


# -------------------------
# REGION DETECTOR
# -------------------------
def map_region(topic):

    topic = str(topic).lower()

    for k, region in KEYWORD_MAP.items():
        if k in topic:
            return region

    return "global"


# -------------------------
# MAIN ENGINE
# -------------------------
def build_geopolitical_map(signals):

    regions = {}

    for s in signals:

        topic = s.get("text") or "unknown"
        base_score = s.get("score", 0)

        # 🔥 GEOPOLITICAL INTENSITY
        geo = detect_geopolitical_signal(topic)
        geo_score = geo.get("geopolitical_score", 0)

        # 🔥 FINAL SCORE (INTELLIGENCE BOOST)
        final_score = base_score + (geo_score * 2)

        region = map_region(topic)

        regions[region] = regions.get(region, 0) + final_score

    # -------------------------
    # NORMALIZATION
    # -------------------------
    total = sum(regions.values()) or 1

    result = []

    for r, val in regions.items():
        result.append({
            "region": r,
            "score": round(val, 2),
            "ratio": round(val / total, 3)
        })

    result.sort(key=lambda x: x["score"], reverse=True)

    return result
