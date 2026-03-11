from fastapi import FastAPI
import threading

from database.database import init_database
from backend.posts import get_feed, get_post
from backend.topic_api import get_topics
from backend.orchestrator import start as start_orchestrator


app = FastAPI()

init_database()


def run_orchestrator():
    start_orchestrator()


thread = threading.Thread(target=run_orchestrator)
thread.daemon = True
thread.start()


@app.get("/")
def home():
    return {"system": "DynamoHive running"}


@app.get("/feed")
def feed():
    return get_feed()


@app.get("/article/{post_id}")
def article(post_id: int):
    return get_post(post_id)


@app.get("/topics")
def topics():
    return get_topics()
