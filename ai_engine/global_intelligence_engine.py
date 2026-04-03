from fastapi import FastAPI
from backend.feed_engine import get_feed
from backend.events import handle_event

import threading
from backend.auto_content_loop import start as start_loop

app = FastAPI()


# -------------------------
# TEST SIGNALS
# -------------------------
signals = [
    {"topic": "war", "score": 10},
    {"topic": "ai", "score": 8},
    {"topic": "economy", "score": 7},
    {"topic": "politics", "score": 6}
]


# -------------------------
# ROOT
# -------------------------
@app.get("/")
def root():
    return {"status": "DynamoHive running"}


# -------------------------
# FEED
# -------------------------
@app.get("/feed")
def feed(user_id: str):
    return get_feed(user_id, signals)


# -------------------------
# EVENT
# -------------------------
@app.get("/event")
def event(user_id: str, type: str, topic: str):
    return handle_event(user_id, {
        "type": type,
        "topic": topic
    })


# -------------------------
# ORCHESTRATOR START
# -------------------------
@app.on_event("startup")
def start_orchestrator():
    thread = threading.Thread(target=start_loop, daemon=True)
    thread.start()
