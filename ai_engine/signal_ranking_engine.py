import re

from difflib import SequenceMatcher


# -------------------------
# NORMALIZE
# -------------------------
def normalize(text):

    text = str(text).lower()

    text = re.sub(r"http\\S+", "", text)
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\\s+", " ", text).strip()

    return text


# -------------------------
# SIMILARITY
# -------------------------
def similar(a, b, threshold=0.75):

    return (
        SequenceMatcher(None, a, b)
        .ratio()
        >= threshold
    )


# -------------------------
# MAIN RANKER
# -------------------------
def rank_signals(signals):

    if not isinstance(signals, list):
        return []

    ranked = []

    for signal in signals:

        if not isinstance(signal, dict):
            continue

        score = float(
            signal.get("priority", 0.5)
        )

        ranked.append({
            **signal,
            "score": score
        })

    ranked.sort(
        key=lambda x: x.get("score", 0),
        reverse=True
    )

    return ranked
