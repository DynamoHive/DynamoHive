from fastapi import FastAPI

import backend.database

from backend.data_pipeline import start_pipeline
from backend.growth_engine import start_growth
from backend.auto_content_loop import start_content_loop

from backend.events import router as events_router
from backend.posts import router as posts_router
from backend.users import router as users_router

from backend.feed_engine import rank_posts

app = FastAPI()

# sistemleri başlat
start_pipeline()
start_growth()
start_content_loop()

# router bağlantıları
app.include_router(events_router)
app.include_router(posts_router)
app.include_router(users_router)

@app.get("/")
def home():
    return {"platform": "DynamoHive", "status": "running"}

@app.get("/feed")
def get_feed(user_id: str = "guest"):

    posts = rank_posts(user_id)

    return {"posts": posts}

@app.get("/metrics")
def metrics():

    from backend.analytics_engine import get_metrics

    return get_metrics()
