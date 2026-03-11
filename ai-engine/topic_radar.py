from collections import Counter
import re


# common stopwords (ignored words)

STOPWORDS = {
    "the","and","of","to","in","a","for","on","with","at","by","from",
    "is","are","was","were","be","been","this","that","these","those",
    "it","its","as","an","or"
}


def clean_text(text):

    text = text.lower()

    text = re.sub(r"[^a-z0-9\s]", "", text)

    words = text.split()

    words = [w for w in words if w not in STOPWORDS and len(w) > 2]

    return words


def topic_radar(articles):

    words = []

    for article in articles:

        title = article.get("title","")

        words += clean_text(title)

    if not words:
        return []

    counts = Counter(words)

    top = counts.most_common(10)

    topics = []

    for word, score in top:

        topics.append({
            "topic": word,
            "score": score
        })

    return topics
