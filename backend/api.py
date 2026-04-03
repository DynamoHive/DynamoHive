from fastapi import APIRouter
from backend.storage import get_posts
from ai_engine.signal_ranking_engine import rank_signals

router = APIRouter()


@router.get("/posts")
def get_posts_api():

    try:
        posts = get_posts()
        print("POST COUNT:", len(posts))
    except Exception as e:
        print("GET_POSTS ERROR:", e)
        return {"posts": []}

    signals = []

    for p in posts:
        try:
            signals.append({
                "post_id": p.get("id"),
                "content": p,

                # ranking input
                "text": str(p.get("title", "")) + " " + str(p.get("content", "")),
                "keywords": p.get("keywords", []),
                "source": p.get("source", "unknown"),
                "timestamp": p.get("timestamp", 0),

                "boost": 0
            })
        except Exception as e:
            print("SIGNAL BUILD ERROR:", e)

    print("SIGNAL COUNT:", len(signals))

    # 🔴 RANKING (FAIL-SAFE)
    try:
        ranked = rank_signals(signals)
    except Exception as e:
        print("RANK ERROR:", e)
        ranked = signals  # fallback

    # 🔴 BOŞSA fallback
    if not ranked:
        print("RANK EMPTY → FALLBACK TO RAW POSTS")
        return {"posts": posts}

    # 🔴 NORMAL AKIŞ
    try:
        ranked_posts = [s.get("content") for s in ranked if s.get("content")]
    except Exception as e:
        print("POST EXTRACT ERROR:", e)
        return {"posts": posts}

    return {"posts": ranked_posts}


@router.get("/posts/{post_id}")
def get_post(post_id: int):

    try:
        posts = get_posts()
    except:
        return {"error": "data error"}

    for p in posts:
        if p.get("id") == post_id:
            return p

    return {"error": "post not found"}
