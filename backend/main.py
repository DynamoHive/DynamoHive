from fastapi import FastAPI
import threading

from backend.orchestrator import DynamoHiveCore
from backend.feed_engine import get_feed


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
