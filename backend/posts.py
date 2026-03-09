from fastapi import APIRouter
from backend.data_pipeline import add_event

router = APIRouter()

posts = []

@router.post("/posts")
def create_post(user_id: int, content: str):

    post = {
        "id": len(posts) + 1,
        "user_id": user_id,
        "content": content
    }

    posts.append(post)

    add_event({
        "type": "post_create",
        "user_id": user_id,
        "post_id": post["id"]
    })

    return post


@router.get("/posts")
def list_posts():
    return posts
