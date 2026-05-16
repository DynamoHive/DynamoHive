from fastapi import APIRouter, HTTPException

from backend.storage import get_signals
from ai_engine.signal_ranking_engine import rank_signals

router = APIRouter()


# =====================================================
# SIGNALS LIST (formerly posts)
# =====================================================
@router.get("/posts")
def get_posts_api():

    signals = get_signals() or []

    prepared = []

    for s in signals:

        if not isinstance(s, dict):
            continue

        title = s.get("title", "")
        content = s.get("content", "")

        prepared.append({
            "signal_id": s.get("id"),
            "title": title,
            "content": content,
            "text": f"{title} {content}",
            "source": "internal",
            "timestamp": s.get("timestamp", 0),
            "priority": s.get("priority", 0.5)
        })

    ranked = rank_signals(prepared) or []

    ranked_signals = [
        s for s in ranked
        if isinstance(s, dict)
    ]

    return {
        "count": len(ranked_signals),
        "data": ranked_signals
    }


# =====================================================
# SINGLE SIGNAL
# =====================================================
@router.get("/posts/{signal_id}")
def get_post(signal_id: int):

    signals = get_signals() or []

    for s in signals:

        if not isinstance(s, dict):
            continue

        if s.get("id") == signal_id:
            return s

    raise HTTPException(
        status_code=404,
        detail="signal not found"
    )
