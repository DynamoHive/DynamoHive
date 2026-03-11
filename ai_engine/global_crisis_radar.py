CRISIS_KEYWORDS = {

    "war_risk": [
        "military escalation",
        "troop mobilization",
        "airstrike",
        "missile attack",
        "border conflict"
    ],

    "economic_crisis": [
        "bank collapse",
        "inflation surge",
        "debt crisis",
        "market crash",
        "economic collapse"
    ],

    "cyber_warfare": [
        "cyber attack",
        "critical infrastructure hack",
        "state hackers",
        "ransomware attack"
    ],

    "diplomatic_crisis": [
        "sanctions escalation",
        "diplomatic expulsion",
        "embassy closure",
        "treaty breakdown"
    ]
}


def detect_global_crisis(text):

    text = text.lower()

    results = {}

    for category, keywords in CRISIS_KEYWORDS.items():

        score = 0

        for k in keywords:

            if k in text:
                score += 1

        results[category] = score

    return results
