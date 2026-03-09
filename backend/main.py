from fastapi import FastAPI
from importlib import import_module
from backend.data_pipeline import start_pipeline

app = FastAPI()

# pipeline başlat
start_pipeline()

ai_module = import_module("ai-engine.recommendation")

@app.get("/")
def home():
    return {"platform": "DynamoHive", "status": "running"}

@app.get("/feed")
def get_feed(user_id: int = 1):
    return ai_module.recommend_posts(user_id)
