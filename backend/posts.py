from fastapi import APIRouter

router = APIRouter()

posts = []

@router.post("/posts/create")
def create_post(content: str):
    post = {"id": len(posts) + 1, "content": content}
    posts.append(post)
    return post

@router.get("/posts")
def list_posts():
    return posts
