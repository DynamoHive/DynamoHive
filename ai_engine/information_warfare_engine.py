import re

# -------------------------
# 🔥 PATTERNS
# -------------------------

PROPAGANDA_PATTERNS = [
    r"\btraitor\b",
    r"\benemy\b",
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

NARRATIVE_PATTERNS = {
    "anti_west": [
        r"\bwestern propaganda\b",
        r"\banti west\b",
        r"\bwest is collapsing\b"
    ],
    "anti_system": [
        r"\bcorrupt system\b",
        r"\bthey control everything\b"
    ],
    "fear_control": [
        r"\bthey are coming\b",
        r"\bthis is the end\b",
        r"\btotal collapse\b"
    ]
}


# -------------------------
# 🔥 MAIN ENGINE
# -------------------------

def detect_information_warfare(text):

    if not text:
        return _empty()

    text = str(text).lower()

    propaganda_hits = 0
    coordination_hits = 0
    narratives = []

    # -------------------------
    # PROPAGANDA
    # -------------------------
    for p in PROPAGANDA_PATTERNS:
        if re.search(p, text):
            propaganda_hits += 1

    # -------------------------
    # COORDINATED BEHAVIOR
    # -------------------------
    for p in COORDINATED_PATTERNS:
        if re.search(p, text):
            coordination_hits += 1

    # -------------------------
    # NARRATIVE DETECTION 🔥
    # -------------------------
    for name, patterns in NARRATIVE_PATTERNS.items():
        for p in patterns:
            if re.search(p, text):
                narratives.append(name)
                break

    # -------------------------
    # SCORE
    # -------------------------
    score = (propaganda_hits * 2) + (coordination_hits * 2) + len(narratives)

    level = _classify(score)

    return {
        "propaganda_hits": propaganda_hits,
        "coordination_hits": coordination_hits,
        "narratives": list(set(narratives)),
        "score": score,
        "level": level,
        "flagged": score >= 3
    }


# -------------------------
# 🔥 CLASSIFICATION
# -------------------------
def _classify(score):

    if score >= 6:
        return "high"

    if score >= 3:
        return "medium"

    return "low"


def _empty():
    return {
        "propaganda_hits": 0,
        "coordination_hits": 0,
        "narratives": [],
        "score": 0,
        "level": "none",
        "flagged": False
    }
