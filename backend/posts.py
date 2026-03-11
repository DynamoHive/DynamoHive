from database.database import get_posts, get_post


def get_feed():

    posts = get_posts()

    feed = []

    for p in posts:

        feed.append({
            "id": p[0],
            "title": p[1]
        })

    return feed


def get_post_by_id(post_id):

    post = get_post(post_id)

    if not post:
        return None

    return {
        "id": post[0],
        "title": post[1],
        "content": post[2]
    }
