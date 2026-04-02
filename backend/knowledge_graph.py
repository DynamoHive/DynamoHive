graph = {}


def add_knowledge(topic, post_id=None):

    global graph

    if not topic:
        return

    topic = str(topic).lower().strip()

    if topic not in graph:
        graph[topic] = {
            "connections": [],
            "posts": []
        }

    # post bağlantısı
    if post_id and post_id not in graph[topic]["posts"]:
        graph[topic]["posts"].append(post_id)

    print(f"Knowledge added: {topic} -> post {post_id}")
