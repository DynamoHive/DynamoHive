from fastapi import FastAPI
import threading

from database.database import init_database
from backend.posts import get_feed, get_post_by_id
from backend.topic_api import get_topics
from backend.orchestrator import start as start_orchestrator


app = FastAPI(title="DynamoHive Intelligence Platform")


# database başlat
init_database()


def run_orchestrator():
    try:
        start_orchestrator()
    except Exception as e:
        print("Orchestrator error:", e)


@app.on_event("startup")
def start_background_tasks():

    thread = threading.Thread(target=run_orchestrator)
    thread.daemon = True
    thread.start()

    print("Orchestrator thread started")


@app.get("/")
def home():
    return {"system": "DynamoHive running"}


@app.get("/feed")
def feed():
    return get_feed()


@app.get("/article/{post_id}")
def article(post_id: int):

    post = get_post_by_id(post_id)

    if not post:
        return {"error": "post not found"}

    return post


@app.get("/topics")
def topics():
    return get_topics()


@app.get("/health")
def health():
    return {"status": "ok"}
