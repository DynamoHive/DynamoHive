from fastapi import FastAPI
from backend.orchestrator import DynamoHiveCore
from backend.feed_engine import get_feed
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

    return {
        "platform": "DynamoHive",
        "status": "running"
    }


@app.get("/feed")
def feed():

    return get_feed()
