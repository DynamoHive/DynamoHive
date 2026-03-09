from collections import defaultdict

from backend.knowledge_graph import get_graph

topic_popularity = defaultdict(int)


def update_map():

    graph = get_graph()

    for topic, posts in graph.items():

        topic_popularity[topic] = len(posts)


def get_map():

    update_map()

    result = []

    for topic, count in topic_popularity.items():

        result.append({
            "topic": topic,
            "posts": count
        })

    result.sort(reverse=True, key=lambda x: x["posts"])

    return result
