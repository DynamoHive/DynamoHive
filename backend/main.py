from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import threading
import time
import traceback

from backend.orchestrator import Orchestrator


# -------------------------
# APP
# -------------------------

app = FastAPI()


# -------------------------
# CORS FIX
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# GLOBAL ORCHESTRATOR
# -------------------------

orchestrator = Orchestrator()

LATEST_DATA = []
LAST_UPDATE = 0
CYCLE_COUNT = 0


# -------------------------
# BACKGROUND LOOP
# -------------------------

def run_loop():

    global LATEST_DATA
    global LAST_UPDATE
    global CYCLE_COUNT

    print("🚀 FORCE START")
    print("🔥 ORCHESTRATOR READY")

    while True:

        try:

            CYCLE_COUNT += 1

            print(f"\n🔁 LOOP TICK #{CYCLE_COUNT}")

            data = orchestrator.run_cycle()

            # güvenli cache
            if isinstance(data, list):

                if len(data) > 0:

                    LATEST_DATA = data
                    LAST_UPDATE = int(time.time())

                    print(f"✅ CACHE UPDATED: {len(data)} items")

                else:
                    print("⚠️ EMPTY LIST")

            else:
                print("⚠️ INVALID DATA FORMAT")

        except Exception as e:

            print("❌ LOOP ERROR")
            traceback.print_exc()

        time.sleep(20)


# -------------------------
# STARTUP EVENT
# -------------------------

@app.on_event("startup")
def startup_event():

    print("🔥 STARTUP EVENT")

    thread = threading.Thread(
        target=run_loop,
        daemon=True
    )

    thread.start()

    print("✅ BACKGROUND THREAD STARTED")


# -------------------------
# ROOT
# -------------------------

@app.get("/")
def root():

    return {
        "status": "DynamoHive running",
        "items": len(LATEST_DATA),
        "cycle": CYCLE_COUNT,
        "last_update": LAST_UPDATE
    }


# -------------------------
# INTELLIGENCE FEED
# -------------------------

@app.get("/intel")
def get_intel():

    return JSONResponse({
        "status": "ok",
        "items": len(LATEST_DATA),
        "cycle": CYCLE_COUNT,
        "last_update": LAST_UPDATE,
        "data": LATEST_DATA
    })


# -------------------------
# EVENT FIX
# -------------------------

@app.get("/event")
def event(
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
        "topic": topic
    }


# -------------------------
# HEALTH
# -------------------------

@app.get("/health")
def health():

    return {
        "status": "ok",
        "orchestrator": "active",
        "cycle": CYCLE_COUNT,
        "cached_items": len(LATEST_DATA)
    }
