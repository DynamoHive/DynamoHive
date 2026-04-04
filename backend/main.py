from fastapi import FastAPI
import threading
import time
import traceback

from backend.feed_engine import get_feed
from backend.events import handle_event
from backend.orchestrator import Orchestrator


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
        return {"error": "feed_error", "detail": str(e)}


# -------------------------
# EVENT
# -------------------------
@app.get("/event")
def event(user_id: str, type: str, topic: str):
    try:
        return handle_event(user_id, {"type": type, "topic": topic})
    except Exception as e:
        return {"error": "event_error", "detail": str(e)}


# -------------------------
# HEALTH
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------
# 🔥 START ORCHESTRATOR (INLINE LOOP)
# -------------------------
@app.on_event("startup")
def start_orchestrator():

    def runner():
        print("🚀 THREAD STARTED")

        try:
            orch = Orchestrator()
            print("🔥 ORCHESTRATOR INIT OK")

            while True:
                print("🔁 LOOP TICK")
                try:
                    orch.run_cycle()
                except Exception:
                    print("❌ CYCLE ERROR")
                    traceback.print_exc()

                time.sleep(20)

        except Exception:
            print("❌ LOOP CRASH")
            traceback.print_exc()

    thread = threading.Thread(target=runner)
    thread.start()
