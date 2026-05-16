import time

from fastapi import APIRouter

from backend.storage import get_signals
from ai_engine.signal_ranking_engine import rank_signals

router = APIRouter()


@router.get("/intel")
def get_intel():

    posts = get_signals(limit=100)

    ranked = rank_signals(posts)

    return {
        "cycle": len(ranked),
        "last_update": int(time.time()),
        "data": ranked
    }
