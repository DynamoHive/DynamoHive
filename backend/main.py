from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.logger import logger
from backend.storage import init_db
from backend.services.scheduler import scheduler
from backend.event_pipeline import start_pipeline

from backend.api.intel import router as intel_router
from backend.api.signals import router as signals_router
from backend.api.analytics import router as analytics_router
from backend.api.decision import router as decision_router

app = FastAPI(
    title="DynamoHive",
    version="2.0.0"
)

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# ROUTERS
# -------------------------
app.include_router(intel_router)
app.include_router(signals_router)
app.include_router(analytics_router)
app.include_router(decision_router)

# -------------------------
# STARTUP
# -------------------------
@app.on_event("startup")
def startup_event():

    logger.info("[MAIN] startup")

    init_db()

    start_pipeline()

    scheduler.start()

    logger.info("[MAIN] initialized")


# -------------------------
# ROOT
# -------------------------
@app.get("/")
def root():
    return {
        "service": "DynamoHive",
        "status": "running",
        "version": "2.0.0"
    }


# -------------------------
# HEALTH
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok"}
