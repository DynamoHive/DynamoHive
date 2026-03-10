from fastapi import FastAPI
from backend.orchestrator import DynamoHiveCore
import os

app = FastAPI()

core = DynamoHiveCore()


@app.on_event("startup")
async def startup_event():
    core.start()


@app.get("/")
def home():
    return {"platform": "DynamoHive", "status": "running"}
