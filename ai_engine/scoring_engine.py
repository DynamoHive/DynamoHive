from .dynamic_weights import get_weight

def compute_score(base_score, insights):

    score = base_score

    for i in insights:
        score += get_weight(i["label"]) * i["confidence"]

    # depth bonus
    score += len(insights) * 0.5

    return round(score, 3)
