from collections import defaultdict
import time

narrative_db = defaultdict(list)

KEYWORDS = [
    "war",
    "nato",
    "sanction",
    "ai regulation",
    "cyber attack",
    "economic crisis",
    "propaganda",
    "military"
]


def detect_narratives(text):

    text_lower = text.lower()

    found = []

    for k in KEYWORDS:

        if k in text_lower:
            found.append(k)

    return found


def update_narratives(text):

    narratives = detect_narratives(text)

    now = time.time()

    for n in narratives:

        narrative_db[n].append(now)

    return narratives


def get_trending_narratives():

    result = {}

    for n, times in narrative_db.items():

        result[n] = len(times)

    return sorted(result.items(), key=lambda x: x[1], reverse=True)
