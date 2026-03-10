import threading
import time
import random

from backend.knowledge_graph import add_knowledge

global_topics = [
    "ai",
    "climate",
    "energy",
    "economy",
    "technology",
    "science",
    "space",
    "robotics"
]


def scan_trends():

    topic = random.choice(global_topics)

    add_knowledge(topic, "radar")

    print("Radar detected topic:", topic)


def radar_loop():

    while True:

        scan_trends()

        time.sleep(90)


def start_radar():

    worker = threading.Thread(target=radar_loop)

    worker.daemon = True

    worker.start()
