 return {"error": str(e)}

    for p in posts:
        if p.get("id") == post_id:
            return {
                "id": p.get("id"),
                "title": p.get("title"),
                "content": p.get("content"),
                "created_at": p.get("created_at"),
            }

    return {"error": "post not found"}


# 🔥 DEBUG (SİLME, LAZIM)
@router.get("/debug/posts")
def debug_posts():
    try:
        return {"raw": get_posts()}
    except Exception as e:
        return {"error": str(e)}
