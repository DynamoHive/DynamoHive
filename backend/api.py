from fastapi import APIRouter, HTTPException

from backend.storage import get_signals  # ❗ get_posts YOK
from ai_engine.signal_ranking_engine import rank_signals

router = APIRouter()


# -------------------------
# INTEL FEED
# -------------------------
@router.get("/intel")
def get_intel():

    posts = get_signals(limit=100) or []

    signals = []

    for p in posts:

        if not isinstance(p, dict):
            continue

        title = p.get("title", "")
        content = p.get("content", "")

        signals.append({
            "post_id": p.get("id"),
            "topic": p.get("topic", title),
            "text": f"{title} {content}",
            "content": content,
            "score": float(p.get("priority", 0.5)),
            "sources": [],
            "timestamp": p.get("timestamp", 0),
        })

    ranked = rank_signals(signals) or []

    return {
        "cycle": len(ranked),
        "data": ranked,
        "last_update": int(__import__("time").time())
    }


# -------------------------
# SINGLE POST
# -------------------------
@router.get("/intel/{post_id}")
def get_intel_item(post_id: int):

    posts = get_signals(limit=200) or []

    for p in posts:
        if p.get("id") == post_id:
            return p

    raise HTTPException(status_code=404, detail="not found")
