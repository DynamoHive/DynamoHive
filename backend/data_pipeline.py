from collections import defaultdict
import time

trust_scores = defaultdict(lambda: 1.0)
user_activity = defaultdict(list)

SPAM_WINDOW = 10
SPAM_LIMIT = 20

def update_trust(event):

    user_id = event.get("user_id")
    event_type = event.get("type")

    if not user_id:
        return

    now = time.time()

    user_activity[user_id].append(now)

    # sadece son zaman aralığını tut
    user_activity[user_id] = [
        t for t in user_activity[user_id]
        if now - t < SPAM_WINDOW
    ]

    # çok fazla event varsa trust düşür
    if len(user_activity[user_id]) > SPAM_LIMIT:
        trust_scores[user_id] *= 0.9

def get_trust(user_id):

    return trust_scores[user_id]   
