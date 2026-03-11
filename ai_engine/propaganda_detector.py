propaganda_keywords = [
    "traitor",
    "enemy",
    "collapse",
    "fake news",
    "propaganda",
    "regime"
]


def detect_propaganda(text):

    text_lower = text.lower()

    score = 0

    for k in propaganda_keywords:

        if k in text_lower:
            score += 1

    return {
        "propaganda_score": score,
        "flagged": score >= 2
    }
