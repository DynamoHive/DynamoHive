def analyse(data):

    analysis = []

    for item in data:

        analysis.append({
            "text": item["content"],
            "score": len(item["content"])
        })

    return analysis
