graph = {}


def add_knowledge(topic, post_id):

    if not topic or not post_id:
        return

    topic = str(topic).lower().strip()

    if topic not in graph:
        graph[topic] = []

    graph[topic].append(post_id)


def get_graph():
    return graph
