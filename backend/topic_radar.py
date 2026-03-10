import threading
import time
import random

from backend.knowledge_graph import add_knowledge


GLOBAL_TOPICS = [
    "artificial intelligence",
    "climate change",
    "renewable energy",
    "space exploration",
    "robotics",
    "biotechnology",
    "quantum computing",
    "global economy",
    "cyber security",
    "digital democracy"
]


def scan_trends():

    topic = random.choice(GLOBAL_TOPICS)

    add_knowledge(topic, "radar")

    print("RADAR topic detected:", topic)


def radar_loop():

    while True:

        try:

            scan_trends()

        except Exception as e:

            print("Radar error:", e)

        time.sleep(120)


def start_radar():

    worker = threading.Thread(target=radar_loop)

    worker.daemon = True

    worker.start()

    print("GLOBAL TOPIC RADAR STARTED")


