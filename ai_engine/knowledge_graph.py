from collections import defaultdict

# topic ilişkilerini tutar
GRAPH = defaultdict(set)


def update_graph(post):

    topic = post.get("topic")
    content = post.get("content", "")

    if not topic:
        return

    words = content.lower().split()

    # içerikte geçen kelimelerle ilişki kur
    for w in words:

        if len(w) < 4:
            continue

        GRAPH[topic].add(w)

    print("knowledge graph updated:", topic)



def get_related(topic):

    return list(GRAPH.get(topic, []))[:10]
