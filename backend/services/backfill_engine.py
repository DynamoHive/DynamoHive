from backend.logger import logger
from backend.storage import get_last_signals
from ai_engine.multi_crawler import crawl

class BackfillEngine:

    def __init__(self):
        self.last_backfill_time = 0
        self.backfill_interval = 300  # 5 min

    def should_backfill(self, data):
        return not data

    def run(self):
        logger.info("[BACKFILL] triggered")

        fresh = crawl()

        if fresh:
            logger.info("[BACKFILL] fresh data recovered")
            return fresh

        # fallback to memory layer (NOT cache spam)
        old = get_last_signals(limit=20)

        logger.warning("[BACKFILL] using historical intelligence layer")

        return old or []
