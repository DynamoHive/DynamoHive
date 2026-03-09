events_processed = 0

def register_event():

    global events_processed
    events_processed += 1

def get_metrics():

    return {
        "events_processed": events_processed
    }
