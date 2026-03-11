def trend_engine(topics):

    trends = []

    for t in topics:
        trends.append({
            "topic": t,
            "trend_score": 1
        })

    print("Trends detected:", trends)

    return trends
