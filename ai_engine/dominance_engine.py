# ai_engine/dominance_engine.py

def compute_dominance(signals):

    if not signals:
        return []

    results = []

    total_score = sum(s.get("score", 0) for s in signals) or 1

    for s in signals:
        score = s.get("score", 0)
        topic = s.get("text", "")

        dominance = score / total_score

        results.append({
            "topic": topic,
            "score": score,
            "dominance": round(dominance, 4)
        })

    results.sort(key=lambda x: x["dominance"], reverse=True)

    return results
