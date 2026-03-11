import re

PROPAGANDA_PATTERNS = [
    r"\btraitor\b",
    r"\benemy\b",
    r"\bwestern propaganda\b",
    r"\bfake news\b",
    r"\bregime\b",
    r"\bglobalist\b",
    r"\bnazi\b",
    r"\bimperialist\b"
]

COORDINATED_PATTERNS = [
    r"\bshare this everywhere\b",
    r"\beveryone must know\b",
    r"\bspread this\b",
    r"\bthe media is lying\b"
]


def detect_information_warfare(text):

    text = text.lower()

    propaganda_hits = 0
    coordinated_hits = 0

    for p in PROPAGANDA_PATTERNS:
        if re.search(p, text):
            propaganda_hits += 1

    for p in COORDINATED_PATTERNS:
        if re.search(p, text):
            coordinated_hits += 1

    score = propaganda_hits + coordinated_hits

    result = {
        "propaganda_hits": propaganda_hits,
        "coordination_hits": coordinated_hits,
        "score": score
    }

    return result
