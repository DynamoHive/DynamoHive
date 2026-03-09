import threading
import queue

event_queue = queue.Queue()

def process_events():

    while True:

        event = event_queue.get()

        print("Processing event:", event)

        event_queue.task_done()

def start_pipeline():

    worker = threading.Thread(target=process_events)

    worker.daemon = True

    worker.start()
