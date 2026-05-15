import time
import threading
import traceback

from backend.orchestrator import run_pipeline
from backend.logger import logger


class Scheduler:
    def __init__(self, interval: int = 30):
        self.interval = interval
        self.running = False
        self.thread = None

    # -----------------------------
    # START
    # -----------------------------
    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

        logger.info("[SCHEDULER] started")

    # -----------------------------
    # STOP
    # -----------------------------
    def stop(self):
        self.running = False
        logger.info("[SCHEDULER] stopped")

    # -----------------------------
    # MAIN LOOP
    # -----------------------------
    def _loop(self):
        while self.running:
            try:
                logger.info("[SCHEDULER] cycle start")

                result = run_pipeline()

                logger.info(f"[SCHEDULER] cycle done: {result}")

            except Exception as e:
                logger.error("[SCHEDULER] error occurred")
                logger.error(traceback.format_exc())

            time.sleep(self.interval)
