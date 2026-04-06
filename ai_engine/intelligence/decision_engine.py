def should_generate(signal):
    if not isinstance(signal, dict):
        return False

    score = signal.get("score", 0)

    try:
        score = float(score)
    except:
        score = 0

    return score >= 2
