from collections import Counter


TOPIC_MEMORY = Counter()


def learn_topics(post):

    topic = post.get("topic")

    if not topic:
        return

    TOPIC_MEMORY[topic] += 1

    print("topic learning:", dict(TOPIC_MEMORY))


def get_top_topics(limit=5):

    return TOPIC_MEMORY.most_common(limit)
