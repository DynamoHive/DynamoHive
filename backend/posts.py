from database.database import get_posts, get_post


def get_feed():

    posts = get_posts()

    results = []

    for p in posts:

        results.append({
            "id": p[0],
            "title": p[1]
        })

    return results


def get_post(post_id):

    post = get_post(post_id)

    if not post:
        return None

    return {
        "id": post[0],
        "title": post[1],
        "content": post[2]
    }
