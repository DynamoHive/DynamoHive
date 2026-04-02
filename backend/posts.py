from fastapi import APIRouter
from backend.storage import get_posts

router = APIRouter()


@router.get("/posts")
def get_posts_api():

    posts = get_posts()

    return {
        "posts": [
            {
                "id": p["id"],
                "title": p["title"]
            }
            for p in posts
        ]
    }


@router.get("/posts/{post_id}")
def get_post(post_id: int):

    posts = get_posts()

    for p in posts:
        if p["id"] == post_id:
            return {
                "id": p["id"],
                "title": p["title"],
                "content": p["content"],
                "created_at": p["created_at"]
            }

    return {"error": "post not found"}
