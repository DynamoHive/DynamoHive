import re
from difflib import SequenceMatcher


# -------------------------
# NORMALIZATION
# -------------------------
def normalize(text):
    try:
        text = str(text).lower()

        text = re.sub(r"http\\S+", "", text)
        text = re.sub(r"[^a-z0-9 ]", " ", text)
        text = re.sub(r"\\s+", " ", text).strip()

        return text

    except Exception:
        return ""


# -------------------------
# TEXT SIMILARITY
# -------------------------
def similar(a, b, threshold=0.75):
    try:
        return SequenceMatcher(None, a, b).ratio() >= threshold

    except Exception:
        return False


# -------------------------
# SEVERITY CALCULATION
# -------------------------
def calculate_severity(score):

    if score >= 2.5:
        return "high"

    elif score >= 1.2:
        return "medium"

    return "low"


# -------------------------
# SIGNAL MERGE ENGINE
# -------------------------
def merge_ranked_signals(signals):

    try:

        if not isinstance(signals, list):
            return []

        ranked = sorted(
            signals,
            key=lambda x: x.get("score", 0),
            reverse=True
        )

        merged = []

        for signal in ranked:

            if not isinstance(signal, dict):
                continue

            topic_raw = signal.get("topic") or signal.get("text")
            topic = normalize(topic_raw)

            if not topic:
                continue

            found = False

            for existing in merged:

                existing_topic = normalize(
                    existing.get("topic") or existing.get("text")
                )

                if similar(topic, existing_topic):

                    existing["score"] += signal.get("score", 0)

                    existing["count"] = (
                        existing.get("count", 1) + 1
                    )

                    existing["sources"] = list(set(
                        existing.get("sources", []) +
                        signal.get("sources", [])
                    ))

                    existing["severity"] = calculate_severity(
                        existing["score"]
                    )

                    # Longer topic wins
                    if len(str(topic_raw)) > len(
                        str(existing.get("topic", ""))
                    ):
                        existing["topic"] = topic_raw

                    found = True
                    break

            if not found:

                score = signal.get("score", 0)

                merged.append({
                    **signal,
                    "count": 1,
                    "severity": calculate_severity(score),
                    "sources": signal.get("sources", [])
                })

        merged.sort(
            key=lambda x: (
                x.get("score", 0),
                x.get("count", 0)
            ),
            reverse=True
        )

        return merged

    except Exception as e:

        print("signal_ranking_engine error:", e)

        return signals if isinstance(signals, list) else []
