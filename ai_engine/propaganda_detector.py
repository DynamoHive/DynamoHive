import re

# -------------------------
# 🔥 CORE KEYWORDS
# -------------------------

PROPAGANDA_KEYWORDS = [
    "traitor", "enemy", "collapse", "fake news",
    "propaganda", "regime", "terrorist", "threat"
]

EMOTIONAL_WORDS = [
    "shocking", "outrage", "disaster", "catastrophe",
    "unbelievable", "horrific", "terrifying"
]

ABSOLUTE_WORDS = [
    "always", "never", "everyone", "no one",
    "completely", "totally"
]

US_VS_THEM = [
    "they", "them", "those people", "these people"
]

# -------------------------
# 🔥 MAIN DETECTOR
# -------------------------

def detect_propaganda(text):

    if not text:
        return _empty()

    text_lower = str(text).lower()

    score = 0
    signals = []

    # -------------------------
    # 1. KEYWORD MATCH
    # -------------------------
    for k in PROPAGANDA_KEYWORDS:
        if k in text_lower:
            score += 2
            signals.append(f"keyword:{k}")

    # -------------------------
    # 2. EMOTIONAL MANIPULATION
    # -------------------------
    for w in EMOTIONAL_WORDS:
        if w in text_lower:
            score += 1
            signals.append(f"emotion:{w}")

    # -------------------------
    # 3. ABSOLUTE LANGUAGE
    # -------------------------
    for w in ABSOLUTE_WORDS:
        if w in text_lower:
            score += 1
            signals.append(f"absolute:{w}")

    # -------------------------
    # 4. US vs THEM PATTERN
    # -------------------------
    for w in US_VS_THEM:
        if w in text_lower:
            score += 1
            signals.append(f"division:{w}")

    # -------------------------
    # 5. EXCESSIVE CAPS
    # -------------------------
    if re.search(r"\b[A-Z]{4,}\b", text):
        score += 1
        signals.append("caps")

    # -------------------------
    # 6. EXCLAMATION SPAM
    # -------------------------
    if text.count("!") >= 2:
        score += 1
        signals.append("exclamation")

    # -------------------------
    # 🔥 FINAL CLASSIFICATION
    # -------------------------

    level = _classify(score)

    return {
        "propaganda_score": score,
        "level": level,
        "flagged": score >= 3,
        "signals": signals
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
        "propaganda_score": 0,
        "level": "none",
        "flagged": False,
        "signals": []
    }
