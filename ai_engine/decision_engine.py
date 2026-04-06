def run_decision_pipeline(items):

    if not isinstance(items, list):
        return []

    output = []

    for item in items:

        if not isinstance(item, dict):
            continue

        score = item.get("score", 0)

        try:
            score = float(score)
        except:
            score = 0

        # ANA KARAR LOGIC
        if score >= 5:
            item["decision"] = "generate"
            item["dominant"] = True
            output.append(item)
        else:
            item["decision"] = "ignore"
            item["dominant"] = False

    return output
