from collections import defaultdict

from backend.knowledge_graph import get_graph

learning_scores = defaultdict(float)


def update_learning():

    graph = get_graph()

    for topic, posts in graph.items():

        growth = len(posts) * 0.1

        learning_scores[topic] += growth


def get_learning():

    update_learning()

    result = []

    for topic, score in learning_scores.items():

        result.append({
            "topic": topic,
            "score": score
        })

    result.sort(reverse=True, key=lambda x: x["score"])

    return result
