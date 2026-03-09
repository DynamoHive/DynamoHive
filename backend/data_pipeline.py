        print("Processing event:", event)

        event_queue.task_done()

def start_pipeline():
    worker = threading.Thread(target=process_events)
    worker.daemon = True
    worker.start()
