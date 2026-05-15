from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.orchestrator import Orchestrator
from backend.services.scheduler import Scheduler
from backend.storage import init_db

import threading


# =====================================================
# APP INIT
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
# CORE COMPONENTS
# =====================================================

orchestrator = Orchestrator()
scheduler = Scheduler(interval=20)

LOCK = threading.Lock()


# =====================================================
# STARTUP
# =====================================================

@app.on_event("startup")
def startup():

    init_db()

    scheduler.start()


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():
    return {
        "status": "running",
        "service": "DynamoHive"
    }


# =====================================================
# INTEL (LIVE DATA)
# =====================================================

@app.get("/intel")
def intel():

    # scheduler already updates storage/cache via orchestrator
    from backend.storage import get_signals

    data = get_signals(limit=50)

    return {
        "count": len(data),
        "data": data
    }


# =====================================================
# HEALTH
# =====================================================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "engine": "running",
        "scheduler": "active"
    }


# =====================================================
# DEBUG
# =====================================================

@app.get("/debug")
def debug():

    from backend.storage import get_signals

    data = get_signals(limit=5)

    preview = [
        {
            "title": i.get("title"),
            "topic": i.get("topic"),
            "priority": i.get("priority")
        }
        for i in data
    ]

    return {
        "preview": preview
    }
