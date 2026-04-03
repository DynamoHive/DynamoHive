    posts = get_posts()

    # posts → signal formatı
    signals = []
    for p in posts:
        signals.append({
            "post_id": p["id"],
            "score": 0,
            "content": p
        })

    # ranking uygula
    ranked = rank_signals(signals)

    # tekrar post listesine çevir
    ranked_posts = [s["content"] for s in ranked]

    return {"posts": ranked_posts}


@router.get("/posts/{post_id}")
def get_post(post_id: int):

    posts = get_posts()

    for p in posts:
        if p["id"] == post_id:
            return p

    return {"error": "post not found"}
