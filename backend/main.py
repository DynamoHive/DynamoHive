# backend/main.py

from fastapi import FastAPI
from backend.feed_engine import get_feed
from backend.events import handle_event


app = FastAPI()


# -------------------------
# 🔥 TEST SIGNALS (geçici)
# -------------------------

signals = [
    {"topic": "war", "score": 10},
    {"topic": "ai", "score": 8},
    {"topic": "economy", "score": 7},
    {"topic": "politics", "score": 6}
]


# -------------------------
# 🔥 FEED ENDPOINT
# -------------------------

@app.get("/feed")
def feed(user_id: str):
    """
    örnek:
    /feed?user_id=u1
    """
    return get_feed(user_id, signals)


# -------------------------
# 🔥 EVENT ENDPOINT
# -------------------------

@app.post("/event")
def event(user_id: str, type: str, topic: str):
    """
    örnek:
    /event?user_id=u1&type=click&topic=ai
    """

    result = handle_event(user_id, {
        "type": type,
        "topic": topic
    })

    return result


# -------------------------
# 🔥 HEALTH CHECK
# -------------------------

@app.get("/")
def root():
    return {"status": "DynamoHive running"}
