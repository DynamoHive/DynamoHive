from fastapi import APIRouter
from backend.database import cursor, conn

router = APIRouter()

@router.post("/posts/create")
def create_post(user_id: str, content: str):

    cursor.execute(
        "INSERT INTO posts(user_id,content) VALUES (?,?)",
        (user_id, content)
    )

    conn.commit()

    return {"status": "post created"}


@router.get("/posts")
def list_posts():

    rows = cursor.execute(
        "SELECT id,user_id,content FROM posts"
    ).fetchall()

    posts = []

    for r in rows:
        posts.append({
            "id": r[0],
            "user_id": r[1],
            "content": r[2]
        })

    return {"posts": posts}
