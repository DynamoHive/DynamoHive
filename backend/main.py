from fastapi import FastAPI

from backend.data_pipeline import start_pipeline
from backend.growth_engine import start_growth
from backend.viral_engine import start_viral_engine

from backend.events import router as events_router
from backend.posts import router as posts_router
from backend.users import router as users_router

from backend.orchestrator import DynamoHiveCore


app = FastAPI()

# Core orchestrator
core = DynamoHiveCore()


@app.on_event("startup")
async def startup_event():
    core.start()


# router bağlantıları
app.include_router(events_router)
app.include_router(posts_router)
app.include_router(users_router)


@app.get("/")
def home():
    return {"platform": "DynamoHive", "status": "running"}


@app.get("/feed")
def feed():
    return {
        "posts": [
            {"id": 1, "content": "Welcome to DynamoHive"},
            {"id": 2, "content": "AI powered creator platform"}
        ]
    }
