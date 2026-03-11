from fastapi import FastAPI

from database.database import init_database
from backend.posts import get_feed, get_post
from backend.topic_api import get_topics

app = FastAPI()

init_database()


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
