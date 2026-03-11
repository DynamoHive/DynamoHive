topic_scores = {}


def update_topic_authority(topics):

    global topic_scores

    for t in topics:

        if t not in topic_scores:

            topic_scores[t] = 0

        topic_scores[t] += 1


def get_top_topics(top_n=5):

    sorted_topics = sorted(
        topic_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_topics[:top_n]
