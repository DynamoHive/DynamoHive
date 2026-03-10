graph = {}


def update_graph():

    global graph

    topics = [
        "AI regulation",
        "China technology",
        "Middle East geopolitics",
        "Energy markets",
    ]

    for topic in topics:

        if topic not in graph:
            graph[topic] = []

        for other in topics:

            if other != topic and other not in graph[topic]:
                graph[topic].append(other)

    print("Knowledge graph:", graph)


def run():
    update_graph()
