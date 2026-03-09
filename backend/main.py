
app = FastAPI()

start_pipeline()

ai_module = import_module("ai-engine.recommendation")

app.include_router(events_router)
app.include_router(posts_router)
app.include_router(users_router)

@app.get("/")
def home():
    return {"platform": "DynamoHive", "status": "running"}

@app.get("/feed")
def get_feed(user_id: int = 1):
    return ai_module.recommend_posts(user_id)
