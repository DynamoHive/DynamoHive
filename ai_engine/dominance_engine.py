# ai_engine/dominance_engine.py

def compute_dominance(signals):

    total = sum([s.get("score", 0) for s in signals]) or 1

    dominance = []

    for s in signals:
        topic = s.get("text")
        score = s.get("score", 0)

        ratio = round(score / total, 3)

        dominance.append({
            "topic": topic,
            "score": score,
            "dominance": ratio
        })

    dominance.sort(key=lambda x: x["dominance"], reverse=True)

    return dominance
