from fastapi import APIRouter
from backend.storage import get_posts

router = APIRouter()


@router.get("/posts")
def get_posts_api():
    posts = get_posts()
    return {"posts": posts}


@router.get("/posts/{post_id}")
def get_post(post_id: int):

    posts = get_posts()

    for p in posts:
        if p["id"] == post_id:
            return p

    return {"error": "post not found"}
