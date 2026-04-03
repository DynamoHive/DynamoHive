from fastapi import FastAPI
import threading

# mevcut sistem
from backend.feed_engine import get_feed
from backend.events import handle_event
from backend.auto_content_loop import start as start_loop

# 🔥 AI PIPELINE
from ai_engine.signal_detector import detect_signals
from ai_engine.global_intelligence import merge_signals
from backend.newsroom.story_engine import build_story

app = FastAPI()

# -------------------------
# 🔥 GLOBAL MEMORY (ORCHESTRATOR BURAYA YAZACAK)
# -------------------------
GLOBAL_DATA = []


# -------------------------
# ROOT
# -------------------------
@app.get("/")
def root():
    return {"status": "DynamoHive running"}


# -------------------------
# 🔥 FEED (GERÇEK AI FEED)
# -------------------------
@app.get("/feed")
def feed():

    # 1. signal çıkar
    signals = detect_signals(GLOBAL_DATA)

    # 2. global merge
    signals = merge_signals(signals)

    # 3. intelligence oluştur
    intelligence = {
        "signals": signals
    }

    # 4. story üret
    story = build_story(intelligence)

    return {
        "story": story,
        "signals": signals[:10],
        "count": len(signals)
    }


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
# 🔥 ORCHESTRATOR START
# -------------------------
@app.on_event("startup")
def start_orchestrator():
    thread = threading.Thread(target=start_loop, daemon=True)
    thread.start()
