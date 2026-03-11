viral_scores = {}


def detect_viral(topics):

    global viral_scores

    viral = []

    for t in topics:

        if t not in viral_scores:
            viral_scores[t] = 0

        viral_scores[t] += 1

        if viral_scores[t] > 5:
            viral.append(t)

    return viral
