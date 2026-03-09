@app.get("/feed")
def get_feed(user_id: str = "guest"):

    posts = rank_posts(user_id)

    return {"posts": posts}
