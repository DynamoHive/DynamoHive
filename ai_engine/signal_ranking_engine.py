import re
from difflib import SequenceMatcher


# -------------------------
# HELPERS
# -------------------------

def normalize(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"http\S+", "", text)  # link temizle
    text = re.sub(r"[^a-z0-9\s]", "", text)  # punctuation temizle
    text = re.sub(r"\s+", " ", text).strip()
    return text


def similarity(a, b):
    if not a or not b:
        return 0
    return SequenceMatcher(None, a, b).ratio()


def is_similar(a, b, threshold=0.75):
    return similarity(a, b) >= threshold


# -------------------------
# MAIN FUNCTION
# -------------------------

def cluster_and_rank(signals):

    if not signals:
        return []

    # -------------------------
    # 1. SAFE COPY + SCORE CHECK
    # -------------------------
    ranked = []
    for s in signals:
        if not isinstance(s, dict):
            continue

        score = s.get("score", 0)

        # 🔥 HARD FILTER (CRITICAL)
        if score < 15:
            continue

        ranked.append({
            **s,
            "score": score,
            "count": 1
        })

    # -------------------------
    # 2. INITIAL SORT
    # -------------------------
    ranked.sort(key=lambda x: x.get("score", 0), reverse=True)

    # -------------------------
    # 3. CLUSTER MERGE
    # -------------------------
    merged = []

    for s in ranked:

        topic_raw = s.get("topic") or s.get("title") or s.get("text") or ""
        topic = normalize(topic_raw)

        if not topic:
            continue

        found = False

        for existing in merged:

            existing_raw = existing.get("topic") or existing.get("title") or existing.get("text") or ""
            existing_topic = normalize(existing_raw)

            # ⚡ FAST CHECK (optimizasyon)
            if topic[:50] == existing_topic[:50]:
                sim = 1.0
            else:
                sim = similarity(topic, existing_topic)

            if sim >= 0.75:
                # -------------------------
                # 🔥 MERGE LOGIC
                # -------------------------
                existing["score"] += s.get("score", 0)
                existing["count"] += 1

                # max score sakla (peak signal)
                existing["max_score"] = max(
                    existing.get("max_score", 0),
                    s.get("score", 0)
                )

                # source aggregation
                existing_sources = set(existing.get("sources", []))
                new_sources = set(s.get("sources", []))
                existing["sources"] = list(existing_sources | new_sources)

                found = True
                break

        if not found:
            merged.append({
                **s,
                "count": 1,
                "max_score": s.get("score", 0),
                "sources": s.get("sources", [])
            })

    # -------------------------
    # 4. EVENT / SPIKE SCORE
    # -------------------------
    for m in merged:
        count = m.get("count", 1)

        # 🔥 spike logic
        m["spike_score"] = min(count * 2, 20)

        # final score recompute
        m["final_score"] = (
            m.get("score", 0)
            + m["spike_score"]
        )

    # -------------------------
    # 5. FINAL SORT
    # -------------------------
    merged.sort(key=lambda x: x.get("final_score", 0), reverse=True)

    return merged
