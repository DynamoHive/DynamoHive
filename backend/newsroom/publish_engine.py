# backend/newsroom/publish_engine.py

from backend.storage import save_post


def publish(article):

    if not article:
        return None

    post = {
        "title": "DynamoHive Intelligence",
        "content": article
    }

    save_post(post)

    return post
