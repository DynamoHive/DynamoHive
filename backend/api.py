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

            # ranking için veri
            "text": str(p.get("title", "")) + " " + str(p.get("content", "")),
            "keywords": p.get("keywords", []),
            "source": p.get("source", "unknown"),
            "timestamp": p.get("timestamp", 0),

            # event sonrası kullanılacak
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
