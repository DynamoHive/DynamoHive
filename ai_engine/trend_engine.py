trend_scores = {}


def update_trends(topics):

    global trend_scores

    for t in topics:

        if t not in trend_scores:
            trend_scores[t] = 0

        trend_scores[t] += 1


def get_trending(top_n=5):

    sorted_trends = sorted(
        trend_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_trends[:top_n]
