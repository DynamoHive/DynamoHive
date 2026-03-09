ai_module = import_module("ai-engine.recommendation")

@app.get("/")
def home():
    return {"platform": "DynamoHive", "status": "running"}

@app.get("/feed")
def get_feed(user_id: int = 1):
    return ai_module.recommend_posts(user_id)

app.include_router(user_router)
app.include_router(post_router)
app.include_router(event_router)

