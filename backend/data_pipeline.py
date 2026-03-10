import threading
import queue
import time

from backend.trust_engine import update_trust

event_queue = queue.Queue()


def add_event(event):

    event_queue.put(event)


def process_events():

    while True:

        event = event_queue.get()

        try:

            update_trust(event)

            print("Processing event:", event)

        except Exception as e:

            print("Pipeline error:", e)

        event_queue.task_done()


def start_pipeline():

    worker = threading.Thread(target=process_events)

    worker.daemon = True

    worker.start()

    print("Event pipeline started")
