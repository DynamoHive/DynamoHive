graph = {}


def add_knowledge(data):
    """
    🔥 dışarıdan gelen bilgiyi graph'a ekler
    """
    global graph

    if not data:
        return

    # topic çıkar
    topic = None

    if isinstance(data, dict):
        topic = data.get("topic") or data.get("title")
    elif isinstance(data, str):
        topic = data

    if not topic:
        return

    topic = str(topic).lower().strip()

    if topic not in graph:
        graph[topic] = []

    print(f"Knowledge added: {topic}")


def update_graph():

    global graph

    topics = [
        "ai regulation",
        "china technology",
        "middle east geopolitics",
        "energy markets",
    ]

    for topic in topics:

        topic = topic.lower().strip()

        if topic not in graph:
            graph[topic] = []

        for other in topics:

            other = other.lower().strip()

            if other != topic and other not in graph[topic]:
                graph[topic].append(other)

    print("Knowledge graph:", graph)


def run():
    update_graph()
