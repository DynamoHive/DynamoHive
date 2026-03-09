import queue
import threading

from backend.analytics_engine import record_event
from backend.trust_engine import update_trust
from backend.growth_engine import record_engagement

event_queue = queue.Queue()

def add_event(event):
    event_queue.put(event)

def process_events():
    while True:
        event = event_queue.get()

        print("Processing event:", event)

        record_event(event)
        update_trust(event)
        record_engagement(event.get("user_id"))

        event_queue.task_done()

def start_pipeline():
    worker = threading.Thread(target=process_events)
    worker.daemon = True
    worker.start()
