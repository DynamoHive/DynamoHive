import threading
import queue
import traceback

from backend.logger import logger
from backend.trust_engine import update_trust


# =====================================================
# GLOBAL EVENT QUEUE
# =====================================================
event_queue = queue.Queue()

_worker_started = False
_lock = threading.Lock()


# =====================================================
# ADD EVENT
# =====================================================
def add_event(event):

    try:
        event_queue.put(event)

    except Exception:
        logger.error("[EVENT PIPELINE] add_event failed")
        logger.error(traceback.format_exc())


# =====================================================
# PROCESS EVENTS
# =====================================================
def process_events():

    logger.info("[EVENT PIPELINE] worker started")

    while True:

        try:

            event = event_queue.get(timeout=5)

        except queue.Empty:
            continue

        try:

            update_trust(event)

            logger.info(
                f"[EVENT PIPELINE] processed: "
                f"{event.get('title', 'unknown')}"
            )

        except Exception:

            logger.error("[EVENT PIPELINE ERROR]")
            logger.error(traceback.format_exc())

        finally:

            event_queue.task_done()


# =====================================================
# START PIPELINE
# =====================================================
def start_pipeline():

    global _worker_started

    with _lock:

        if _worker_started:
            return

        worker = threading.Thread(
            target=process_events,
            daemon=True
        )

        worker.start()

        _worker_started = True

        logger.info("[EVENT PIPELINE] started")
