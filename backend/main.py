from fastapi import FastAPI
from backend.orchestrator import DynamoHiveCore
import threading

app = FastAPI()

core = DynamoHiveCore()


@app.on_event("startup")
def start_system():
    thread = threading.Thread(target=core.start)
    thread.daemon = True
    thread.start()


@app.get("/")
def root():
    return {"platform": "DynamoHive", "status": "running"}
