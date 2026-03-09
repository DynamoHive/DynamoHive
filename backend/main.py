from backend.feed_engine import rank_postsfrom fastapi import FastAPI
from backend.data_pipeline import start_pipeline
from backend.events import router as events_router
from backend.posts import router as posts_router
from backend.users import router as users_router
from backend.growth_engine import start_growth

app = FastAPI()

# pipeline başlat
start_pipeline()

# growth engine başlat
start_growth()

# router bağlantıları
app.include_router(events_router)
app.include_router(posts_router)
app.include_router(users_router)

@app.get("/")
def home():
    return {"platform": "DynamoHive", "status": "running"}

@app.get("/feed")
def get_feed():
    return {
        "posts": [
            {"id": 1, "content": "Welcome to DynamoHive"},
            {"id": 2, "content": "AI powered creator platform"}
        ]
    }

@app.get("/metrics")
def metrics():

    from backend.analytics_engine import get_metrics

    return get_metrics()


