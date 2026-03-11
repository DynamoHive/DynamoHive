import re
from collections import Counter


# basit topic sözlüğü
TOPIC_KEYWORDS = {

    "ai": [
        "ai", "artificial intelligence", "machine learning",
        "neural network", "deep learning"
    ],

    "china-tech": [
        "china", "huawei", "tencent", "alibaba", "baidu"
    ],

    "energy-transition": [
        "renewable", "solar", "wind", "energy transition",
        "green energy"
    ],

    "geopolitics": [
        "nato", "sanctions", "war", "geopolitics", "conflict"
    ]

}


def normalize(text):

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    return text


def detect_topics(data):

    topic_scores = Counter()

    for item in data:

        text = normalize(item.get("text", ""))

        for topic, keywords in TOPIC_KEYWORDS.items():

            for keyword in keywords:

                if keyword in text:

                    topic_scores[topic] += 1

    topics = []

    for topic, score in topic_scores.items():

        topics.append({

            "topic": topic,
            "score": score

        })

    topics.sort(key=lambda x: x["score"], reverse=True)

    print("topics detected:", topics)

    return topics
