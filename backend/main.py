from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.services.scheduler import Scheduler

app = FastAPI(title="DynamoHive", version="1.0.0")

scheduler = Scheduler(interval=20)

# =====================================================
# CORS
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# STARTUP
# =====================================================
@app.on_event("startup")
def startup():
    scheduler.start()

# =====================================================
# ROOT
# =====================================================
@app.get("/")
def root():
    return {"status": "running"}

# =====================================================
# INTEL ENDPOINT
# =====================================================
@app.get("/intel")
def intel():
    return {"data": scheduler.orchestrator.run_cycle()}

# =====================================================
# HEALTH
# =====================================================
@app.get("/health")
def health():
    return {"status": "ok"}
