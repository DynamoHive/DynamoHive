memory = {}

def learn_from_topics(topics):

    global memory

    for t in topics:

        if t not in memory:
            memory[t] = 0

        memory[t] += 1

    print("Topic memory:", memory)


def best_topics():

    ranked = sorted(memory.items(), key=lambda x: x[1], reverse=True)

    return ranked[:5]


def run():

    topics = [
        "AI regulation",
        "Energy crisis",
        "China technology",
        "Middle East geopolitics"
    ]

    learn_from_topics(topics)

    print("Top topics:", best_topics())
