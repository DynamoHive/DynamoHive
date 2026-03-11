from fastapi import FastAPI
import threading

from database.database import init_database
from backend.posts import get_feed, get_post
from backend.topic_api import get_topics
from backend.orchestrator import start as start_orchestrator


app = FastAPI(title="DynamoHive API")

# database başlat
init_database()


# orchestrator thread
def run_orchestrator():
    start_orchestrator()


orchestrator_thread = threading.Thread(target=run_orchestrator)
orchestrator_thread.daemon = True
orchestrator_thread.start()


@app.get("/")
def home():
    return {"system": "DynamoHive running"}


@app.get("/feed")
def feed():
    return {"posts": get_feed()}


@app.get("/article/{post_id}")
def article(post_id: int):

    post = get_post(post_id)

    if not post:
        return {"error": "post not found"}

    return post


@app.get("/topics")
def topics():
    return {"topics": get_topics()}
