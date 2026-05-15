from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.logger import logger
from backend.storage import init_db
from backend.services.scheduler import scheduler
from backend.event_pipeline import start_pipeline


# =====================================================
# FASTAPI APP
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
# STARTUP
# =====================================================
@app.on_event("startup")
def startup_event():

    logger.info("[MAIN] startup event")

    # DB INIT
    init_db()
    logger.info("[DB] initialized")

    # EVENT PIPELINE (IMPORTANT: background thread)
    try:
        start_pipeline()
        logger.info("[EVENT PIPELINE] started")
    except Exception as e:
        logger.error("[EVENT PIPELINE ERROR STARTING]")
        logger.error(str(e))

    # SCHEDULER
    try:
        scheduler.start()
        logger.info("[SCHEDULER] started")
    except Exception as e:
        logger.error("[SCHEDULER ERROR STARTING]")
        logger.error(str(e))

    logger.info("[MAIN] system initialized")


# =====================================================
# ROOT
# =====================================================
@app.get("/")
def root():
    return {
        "status": "running",
        "service": "DynamoHive",
        "version": "1.0.0"
    }


# =====================================================
# HEALTH
# =====================================================
@app.get("/health")
def health():
    return {
        "status": "ok"
    }
