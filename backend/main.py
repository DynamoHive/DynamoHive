from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.logger import logger
from backend.storage import init_db
from backend.services.scheduler import scheduler
from backend.event_pipeline import start_pipeline

from backend.api.intel import router as intel_router


app = FastAPI(
    title="DynamoHive",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTES
app.include_router(intel_router)


@app.on_event("startup")
def startup_event():

    logger.info("[MAIN] startup event")

    init_db()
    logger.info("[DB] initialized")

    start_pipeline()
    scheduler.start()

    logger.info("[MAIN] system initialized")


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "DynamoHive",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {"status": "ok"}
