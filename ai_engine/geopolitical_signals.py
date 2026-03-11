geo_keywords = [
    "sanction",
    "military",
    "conflict",
    "war",
    "nato",
    "border",
    "diplomatic"
]


def detect_geopolitical_signal(text):

    text_lower = text.lower()

    score = 0

    for k in geo_keywords:

        if k in text_lower:
            score += 1

    return {
        "geopolitical_score": score,
        "alert": score >= 2
    }
