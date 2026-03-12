from fastapi import FastAPI
from threading import Thread

from backend.orchestrator import start
from database.database import init_database

app = FastAPI(
    title="DynamoHive",
    version="1.0"
)


@app.on_event("startup")
def startup():

    # database başlat
    init_database()

    # orchestrator arka planda başlat
    t = Thread(target=start)
    t.daemon = True
    t.start()


@app.get("/")
def root():

    return {
        "platform": "DynamoHive",
        "status": "running"
    }


@app.get("/health")
def health():

    return {"status": "ok"}

