def detect_topics(data):

    topics = []

    for item in data:

        if "AI" in item["title"]:
            topics.append("ai")

        if "China" in item["title"]:
            topics.append("china-tech")

    return topics
