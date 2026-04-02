from fastapi import APIRouter
from backend.storage import get_posts

router = APIRouter()


@router.get("/posts")
def get_posts_api():
    try:
        posts = get_posts()
    except Exception as e:
        return {"error": str(e)}

    return {
        "posts": [
            {
                "id": p.get("id"),
                "title": p.get("title"),
                "content": p.get("content"),
                "created_at": p.get("created_at"),
            }
            for p in posts
        ]
    }


@router.get("/posts/{post_id}")
def get_post(post_id: int):
    try:
        posts = get_posts()
    except Exception as e:
        return {"error": str(e)}

    for p in posts:
        if p.get("id") == post_id:
            return {
                "id": p.get("id"),
                "title": p.get("title"),
                "content": p.get("content"),
                "created_at": p.get("created_at"),
            }

    return {"error": "post not found"}


# 🔥 DEBUG (SİLME, LAZIM)
@router.get("/debug/posts")
def debug_posts():
    try:
        return {"raw": get_posts()}
    except Exception as e:
        return {"error": str(e)}
