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
# GLOBAL STATE
# =====================================================

orchestrator = Orchestrator()

STATE = {
    "data": [],
    "last_update": 0,
    "cycles": 0,
    "status": "starting"
}

LOCK = threading.Lock()


# =====================================================
# LOOP
# =====================================================

def run_loop():

    print("🚀 DYNAMOHIVE STARTED")
    STATE["status"] = "running"

    while True:
        try:
            STATE["cycles"] += 1

            print(f"🔁 CYCLE #{STATE['cycles']}")

            start = time.time()
            result = orchestrator.run_cycle()
            duration = round(time.time() - start, 2)

            # normalize output
            if isinstance(result, list):
                data = result
            elif isinstance(result, dict):
                data = result.get("signals", [])
            else:
                data = []

            if data:
                with LOCK:
                    STATE["data"] = data
                    STATE["last_update"] = int(time.time())

                print(f"✅ CACHE UPDATED | {len(data)} items | {duration}s")
            else:
                print("⚠️ NOTHING GENERATED")

        except Exception as e:
            STATE["status"] = "error"
            print("❌ LOOP ERROR:", str(e))
            traceback.print_exc()

        time.sleep(20)


# =====================================================
# STARTUP
# =====================================================

@app.on_event("startup")
def startup_event():

    print("🔥 STARTUP EVENT")

    t = threading.Thread(
        target=run_loop,
        daemon=True
    )
    t.start()

    print("✅ BACKGROUND LOOP STARTED")


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():
    with LOCK:
        return STATE


# =====================================================
# INTEL
# =====================================================

@app.get("/intel")
def intel():
    with LOCK:
        return {
            "status": STATE["status"],
            "cycles": STATE["cycles"],
            "last_update": STATE["last_update"],
            "count": len(STATE["data"]),
            "data": STATE["data"]
        }


# =====================================================
# HEALTH
# =====================================================

@app.get("/health")
def health():
    with LOCK:
        return {
            "status": "ok",
            "engine": STATE["status"],
            "cycles": STATE["cycles"]
