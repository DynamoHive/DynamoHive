from fastapi import FastAPI
from backend.orchestrator import DynamoHiveCore
import threading

app = FastAPI()

core = DynamoHiveCore()


def run_core():
    core.start()


@app.on_event("startup")
async def startup_event():

    thread = threading.Thread(target=run_core)
    thread.daemon = True
    thread.start()


@app.get("/")
def home():
    return {"platform": "DynamoHive", "status": "running"}
