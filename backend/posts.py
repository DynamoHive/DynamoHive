from backend.storage import get_posts


def get_feed():

    posts = get_posts()

    feed = []

    for p in posts:

        feed.append({
            "id": p["id"],
            "title": p["title"]
        })

    return feed


def get_post_by_id(post_id):

    posts = get_posts()

    for p in posts:

        if p["id"] == post_id:
            return {
                "id": p["id"],
                "title": p["title"],
                "content": p["content"],
                "created_at": p["created_at"]
            }

    return None
