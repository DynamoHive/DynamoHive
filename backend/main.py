from fastapi import FastAPI
import threading

from backend.feed_engine import get_feed
from backend.events import handle_event
from backend.auto_content_loop import start as start_loop


app = FastAPI()


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
def feed(user_id: str = "global_user"):

    try:
        return get_feed(user_id)
    except Exception as e:
        return {
            "error": "feed_error",
            "detail": str(e)
        }

GLOBAL_DATA = []
# -------------------------
# EVENT
# -------------------------
@app.get("/event")
def event(user_id: str, type: str, topic: str):

    try:
        return handle_event(user_id, {
            "type": type,
            "topic": topic
        })
    except Exception as e:
        return {
            "error": "event_error",
            "detail": str(e)
        }


# -------------------------
# HEALTH (DEBUG)
# -------------------------
@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# -------------------------
# START ORCHESTRATOR
# -------------------------
@app.on_event("startup")
def start_orchestrator():

    def runner():
        try:
            start_loop()
        except Exception as e:
            print("[FATAL LOOP ERROR]", e)

    thread = threading.Thread(target=runner, daemon=True)
    thread.start()
