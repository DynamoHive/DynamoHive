from fastapi import FastAPI
from importlib import import_module

from backend.data_pipeline import start_pipeline
from backend.events import router as events_router
from backend.posts import router as posts_router
from backend.users import router as users_router

app = FastAPI()

# pipeline başlat
start_pipeline()

# AI modülü
ai_module = import_module("ai-engine.recommendation")

# router bağlantıları
app.include_router(events_router)
app.include_router(posts_router)
app.include_router(users_router)

@app.get("/")
def home():
    return {"platform": "DynamoHive", "status": "running"}

@app.get("/feed")
def get_feed(user_id: int = 1):
    return ai_module.recommend_posts(user_id)
