# ai_engine/viral_engine.py

from collections import defaultdict

viral_scores = defaultdict(int)


# -------------------------
# 🔥 VIRAL DETECTION ENGINE
# -------------------------
def detect_viral(signals):

    viral = []

    for s in signals:

        topic = s.get("text") or s.get("topic")

        if not topic:
            continue

        topic = str(topic).lower()

        viral_scores[topic] += 1

        # 🔥 threshold
        if viral_scores[topic] > 5:
            viral.append({
                "topic": topic,
                "viral_score": viral_scores[topic]
            })

    # güçlü olanlar üste
    viral.sort(key=lambda x: x["viral_score"], reverse=True)

    return viral


# -------------------------
# 🔥 VIRAL BOOST (RANKING HOOK)
# -------------------------
def apply_viral_boost(signals, viral_list):

    viral_map = {
        v["topic"]: v["viral_score"]
        for v in viral_list
    }

    for s in signals:

        topic = s.get("text") or s.get("topic")

        if topic in viral_map:
            boost = viral_map[topic] * 0.5  # 🔥 ayarlanabilir

            s["score"] += boost
            s["viral"] = True

    return signals
