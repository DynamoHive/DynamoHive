from collections import defaultdict

user_activity = defaultdict(list)
trust_scores = defaultdict(lambda: 1.0)

SPAM_THRESHOLD = 20

def update_trust(event):

    user_id = event.get("user_id")
    event_type = event.get("type")

    if not user_id:
        return

    user_activity[user_id].append(event_type)

    activity_count = len(user_activity[user_id])

    if activity_count > SPAM_THRESHOLD:
        trust_scores[user_id] *= 0.9


def get_trust_score(user_id):

    return trust_scores[user_id]
