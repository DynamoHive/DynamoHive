trends = []


def detect_trends(topics):

    global trends

    trends = []

    for t in topics:

        if "AI" in t or "technology" in t:
            trends.append(("tech", t))

        if "energy" in t:
            trends.append(("energy", t))

        if "war" in t or "conflict" in t:
            trends.append(("geopolitics", t))

    print("Detected trends:", trends)


def run():

    topics = [
        "AI regulation in Europe",
        "Energy crisis in Europe",
        "China technology strategy",
        "Middle East conflict dynamics"
    ]

    detect_trends(topics)
