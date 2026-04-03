from fastapi import APIRouter
from backend.storage import get_posts
from ai_engine.signal_ranking_engine import rank_signals

router = APIRouter()


@router.get("/posts")
def get_posts_api():

    posts = get_posts()

    signals = []

    for p in posts:
        signals.append({
            "post_id": p.get("id"),
            "content": p,
            "text": str(p.get("title", "")) + " " + str(p.get("content", "")),
            "source": p.get("source", "internal"),
            "timestamp": p.get("timestamp", 0),
            "boost": 0
        })

    ranked = rank_signals(signals)

    ranked_posts = [s["content"] for s in ranked]

    return {"posts": ranked_posts}


@router.get("/posts/{post_id}")
def get_post(post_id: int):

    posts = get_posts()

    for p in posts:
        if p["id"] == post_id:
            return p

    return {"error": "post not found"}
