import threading
import time
import random

from backend.database import cursor, conn

topics = [
    "AI revolution",
    "climate change",
    "future of energy",
    "robotics innovation",
    "space exploration",
    "digital democracy",
    "quantum computing",
    "global economy"
]


def generate_post():

    topic = random.choice(topics)

    content = f"AI insight about {topic}"

    cursor.execute(
        "INSERT INTO posts (content, user_id) VALUES (?, ?)",
        (content, "ai")
    )

    conn.commit()

    print("AI created post:", content)


def content_loop():

    while True:

        try:

            generate_post()

        except Exception as e:

            print("Content loop error:", e)

        time.sleep(90)


def start_content_loop():

    worker = threading.Thread(target=content_loop)

    worker.daemon = True

    worker.start()

    print("AI content engine started")

 
