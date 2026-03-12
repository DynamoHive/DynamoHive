import random


def calculate_trend_score(topic_data):

    if not topic_data:
        return 0

    frequency = topic_data.get("frequency", random.randint(1, 10))
    velocity = topic_data.get("velocity", random.randint(1, 10))
    engagement = topic_data.get("engagement", random.randint(1, 10))

    score = (frequency * 0.4) + (velocity * 0.3) + (engagement * 0.3)

    return round(score, 2)


def is_trending(topic_data):

    score = calculate_trend_score(topic_data)

    if score >= 6:
        return True

    return False
