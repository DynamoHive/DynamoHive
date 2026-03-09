from collections import defaultdict

trust_scores = defaultdict(lambda: 1.0)

def update_trust(event):

    user_id = event.get("user_id")

    if not user_id:
        return

    trust_scores[user_id] *= 0.999


def get_trust(user_id):

    return trust_scores[user_id]
