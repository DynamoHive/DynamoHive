from backend.database import cursor
from backend.trust_engine import get_trust

def rank_posts(user_id):

    rows = cursor.execute(
        "SELECT id,user_id,content FROM posts"
    ).fetchall()

    ranked = []

    for r in rows:

        post = {
            "id": r[0],
            "user_id": r[1],
            "content": r[2],
            "engagement": 1
        }

        trust = get_trust(post["user_id"])

        score = post["engagement"] * trust

        ranked.append((score, post))

    ranked.sort(reverse=True, key=lambda x: x[0])

    return [p[1] for p in ranked]
