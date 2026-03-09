import threading
import queue

from backend.trust_engine import update_trust
from backend.analytics_engine import register_event

event_queue = queue.Queue()


def process_events():

    while True:

        event = event_queue.get()

        update_trust(event)

        register_event()

        print("Processing event:", event)

        event_queue.task_done()


def start_pipeline():

    worker = threading.Thread(target=process_events)

    worker.daemon = True

    worker.start()
