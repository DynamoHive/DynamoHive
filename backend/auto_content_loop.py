import threading
import time

from backend.database import cursor, conn

auto_posts = [
    "AI is shaping the future.",
    "Decentralized media is coming.",
    "Creators will own their audience.",
    "Autonomous platforms are the next step."
]

def generate_post():

    import random

    content = random.choice(auto_posts)

    cursor.execute(
        "INSERT INTO posts(user_id,content) VALUES (?,?)",
        ("ai_system", content)
    )

    conn.commit()

    print("AI posted:", content)


def content_loop():

    while True:

        generate_post()

        time.sleep(60)


def start_content_loop():

    worker = threading.Thread(target=content_loop)

    worker.daemon = True

    worker.start()
