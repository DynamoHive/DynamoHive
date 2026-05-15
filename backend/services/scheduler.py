import time
import threading
import traceback

from backend.logger import logger
from backend.orchestrator import Orchestrator


class Scheduler:

    def __init__(self, interval: int = 20):
        self.interval = interval
        self.running = False
        self.thread = None
        self.orchestrator = Orchestrator()

    # =====================================================
    # START
    # =====================================================
    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

        logger.info("[SCHEDULER] started")

    # =====================================================
    # STOP
    # =====================================================
    def stop(self):
        self.running = False
        logger.info("[SCHEDULER] stopped")

    # =====================================================
    # MAIN LOOP
    # =====================================================
    def _loop(self):
        while self.running:
            try:
                logger.info("[SCHEDULER] cycle start")

                result = self.orchestrator.run_cycle()

                logger.info(f"[SCHEDULER] cycle done | items: {len(result)}")

            except Exception:
                logger.error("[SCHEDULER ERROR]")
                logger.error(traceback.format_exc())

            time.sleep(self.interval)
