import re
from difflib import SequenceMatcher


def normalize(text):
    try:
        text = str(text).lower()
        text = re.sub(r"[^a-z0-9 ]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text
    except:
        return ""


def similar(a, b):
    try:
        return SequenceMatcher(None, a, b).ratio() > 0.75
    except:
        return False


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

        for s in ranked:

            if not isinstance(s, dict):
                continue

            topic_raw = s.get("topic") or s.get("text")
            topic = normalize(topic_raw)

            if not topic:
                continue

            found = False

            for existing in merged:

                existing_topic = normalize(
                    existing.get("topic") or existing.get("text")
                )

                if similar(topic, existing_topic):

                    existing["score"] += s.get("score", 0)
                    existing["count"] = existing.get("count", 1) + 1

                    if len(str(topic_raw)) > len(str(existing.get("topic", ""))):
                        existing["topic"] = topic_raw

                    found = True
                    break

            if not found:
                merged.append({
                    **s,
                    "count": 1
                })

        merged.sort(key=lambda x: x.get("score", 0), reverse=True)

        return merged

    except:
        return signals if isinstance(signals, list) else []
