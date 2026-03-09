from collections import defaultdict

knowledge_graph = defaultdict(list)


def add_knowledge(topic, post_id):

    knowledge_graph[topic].append(post_id)


def get_topic_posts(topic):

    return knowledge_graph[topic]


def get_graph():

    return knowledge_graph
