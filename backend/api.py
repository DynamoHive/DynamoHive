from fastapi import APIRouter, HTTPException
from backend.storage import get_posts
from ai_engine.signal_ranking_engine import rank_signals

router = APIRouter()


@router.get("/posts")
def get_posts_api():

    posts = get_posts() or []

    signals = []

    for p in posts:

        if not isinstance(p, dict):
            continue

        title = p.get("title", "")
        content = p.get("content", "")

        signals.append({
            "post_id": p.get("id"),
            "content": p,
            "text": f"{title} {content}",
            "source": p.get("source", "internal"),
            "timestamp": p.get("timestamp", 0),
            "boost": 0
        })

    ranked = rank_signals(signals) or []

    # güvenli extraction
    ranked_posts = [
        s.get("content", {})
        for s in ranked
        if isinstance(s, dict)
    ]

    return {
        "count": len(ranked_posts),
        "posts": ranked_posts
    }


@router.get("/posts/{post_id}")
def get_post(post_id: int):

    posts = get_posts() or []

    for p in posts:

        if not isinstance(p, dict):
            continue

        if p.get("id") == post_id:
            return p

    raise HTTPException(
        status_code=404,
        detail="post not found"
    )
