from collections import Counter


def topic_radar(articles):

    if not articles:
        return []

    words = []

    for a in articles:
        words += a["title"].lower().split()

    top = Counter(words).most_common(10)

    topics = [w[0] for w in top]

    print("Topic radar:", topics)

    return topics
