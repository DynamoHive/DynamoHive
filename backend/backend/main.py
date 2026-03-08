from fastapi import FastAPI
from backend.users import router as user_router
from backend.posts import router as post_router

app = FastAPI()

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

app.include_router(user_router)
app.include_router(post_router)
from backend.events import router as event_router
