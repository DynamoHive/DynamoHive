from fastapi import FastAPI
import threading

from database.database import init_database
from backend.posts import get_feed, get_post
from backend.topic_api import get_topics
from backend.orchestrator import start as start_orchestrator


app = FastAPI(
    title="DynamoHive",
    description="Autonomous AI Intelligence Platform",
    version="1.0"
)


# DATABASE INIT
init_database()


# ORCHESTRATOR THREAD
orchestrator_started = False


def run_orchestrator():

    global orchestrator_started

    if orchestrator_started:
        return

    orchestrator_started = True

    start_orchestrator()


thread = threading.Thread(target=run_orchestrator)
thread.daemon = True
thread.start()


# HOME
@app.get("/")
def home():

    return {
        "system": "DynamoHive running",
        "status": "online"
    }


# HEALTH CHECK
@app.get("/health")
def health():

    return {"status": "ok"}


# FEED
@app.get("/feed")
def feed():

    return {
        "posts": get_feed()
    }


# ARTICLE
@app.get("/article/{post_id}")
def article(post_id: int):

    post = get_post(post_id)

    if not post:

        return {"error": "post not found"}

    return post


# TOPICS
@app.get("/topics")
def topics():

    return {
        "topics": get_topics()
    }
