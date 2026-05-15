import time
import threading
import traceback

from backend.orchestrator import Orchestrator
from backend.logger import logger


class Scheduler:

    def __init__(self, interval: int = 30):
        self.interval = interval
        self.running = False
        self.thread = None

        # Orchestrator instance (FIX)
        self.orchestrator = Orchestrator()

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

        logger.info("[SCHEDULER] loop active")

        while self.running:

            start = time.time()

            try:
                logger.info("[SCHEDULER] cycle start")

                # FIX: correct orchestrator usage
                result = self.orchestrator.run_cycle()

                if result:
                    logger.info(
                        f"[SCHEDULER] cycle done | items={len(result)} | "
                        f"time={round(time.time() - start, 2)}s"
                    )
                else:
                    logger.info("[SCHEDULER] cycle done | no output")
