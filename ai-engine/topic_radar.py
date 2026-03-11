from collections import Counter

def topic_radar(articles):

    words = []

    for a in articles:
        words += a["title"].lower().split()

    top = Counter(words).most_common(5)

    return [w[0] for w in top]
