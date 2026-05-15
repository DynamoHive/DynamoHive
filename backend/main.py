from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import threading
import time
import traceback

from backend.orchestrator import Orchestrator


# =====================================================
# APP
# =====================================================

app = FastAPI(
    title="DynamoHive",
    version="1.0.0"
)

# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# GLOBALS
# =====================================================

orchestrator = Orchestrator()

LATEST_DATA = []
LAST_UPDATE = 0
CYCLE_COUNT = 0
SYSTEM_STATUS = "starting"

LOCK = threading.Lock()


# =====================================================
# LOOP
# =====================================================

def run_loop():

    global LATEST_DATA, LAST_UPDATE, CYCLE_COUNT, SYSTEM_STATUS

    print("🚀 DYNAMOHIVE STARTED")
    SYSTEM_STATUS = "running"

    while True:
        try:
            CYCLE_COUNT += 1
            print(f"🔁 LOOP TICK #{CYCLE_COUNT}")

            started = time.time()
            data = orchestrator.run_cycle()
            duration = round(time.time() - started, 2)

            if isinstance(data, list) and len(data) > 0:
                with LOCK:
                    LATEST_DATA = data
                    LAST_UPDATE = int(time.time())

                print(f"✅ CACHE UPDATED | {len(data)} items | {duration}s")
            else:
                print("⚠️ EMPTY OR INVALID DATA")

        except Exception as e:
            SYSTEM_STATUS = "error"
            print("❌ LOOP ERROR:", str(e))
            traceback.print_exc()

        time.sleep(20)


# =====================================================
# STARTUP
# =====================================================

@app.on_event("startup")
def startup_event():
    print("🔥 STARTUP EVENT")

    thread = threading.Thread(
        target=run_loop,
        daemon=True
    )
    thread.start()

    print("✅ BACKGROUND THREAD STARTED")


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():
    with LOCK:
        return {
            "status": SYSTEM_STATUS,
            "engine": "DynamoHive",
            "cycles": CYCLE_COUNT,
            "items": len(LATEST_DATA),
            "last_update": LAST_UPDATE
        }


# =====================================================
# INTEL
# =====================================================

@app.get("/intel")
def get_intel():
    with LOCK:
        return JSONResponse({
            "status": SYSTEM_STATUS,
            "items": len(LATEST_DATA),
            "cycle": CYCLE_COUNT,
            "last_update": LAST_UPDATE,
            "data": LATEST_DATA
        })


# =====================================================
# STATS
# =====================================================

@app.get("/stats")
def stats():
    with LOCK:
        return {
            "status": SYSTEM_STATUS,
            "cycles": CYCLE_COUNT,
            "cached_items": len(LATEST_DATA),
            "last_update": LAST_UPDATE
        }


# =====================================================
# EVENT (FIXED)
# =====================================================

@app.get("/event")
def handle_event(
    user_id: str = "",
    type: str = "",
    topic: str = ""
):

    print(
        f"📡 EVENT | user={user_id} | type={type} | topic={topic}"
    )

    return {
        "status": "received",
        "user_id": user_id,
        "type": type,
        "topic": topic,
        "timestamp": int(time.time())
    }


# =====================================================
# HEALTH
# =====================================================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "system": SYSTEM_STATUS,
        "orchestrator": "active",
        "cycle": CYCLE_COUNT,
        "cached_items": len(LATEST_DATA)
    }


# =====================================================
# DEBUG
# =====================================================

@app.get("/debug")
def debug():
    with LOCK:
        preview = []

        for item in LATEST_DATA[:5]:
            if isinstance(item, dict):
                preview.append({
                    "title": item.get("title", ""),
                    "score": item.get("priority", 0),
                    "topic": item.get("topic", "")
                })

        return {
            "status": SYSTEM_STATUS,
            "preview_count": len(preview),
            "preview": preview
        }
