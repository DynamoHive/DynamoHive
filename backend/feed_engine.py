from backend.trust_engine import get_trust

posts_store = [
    {"id": 1, "user_id": "system", "content": "Welcome to DynamoHive", "engagement": 1},
    {"id": 2, "user_id": "system", "content": "AI powered creator platform", "engagement": 1}
]

def rank_posts(user_id):

    ranked = []

    for post in posts_store:

        trust = get_trust(post["user_id"])

        score = post["engagement"] * trust

        ranked.append((score, post))

    ranked.sort(reverse=True, key=lambda x: x[0])

    return [p[1] for p in ranked]
