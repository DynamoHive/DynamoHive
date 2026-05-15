from backend.logger import logger
from backend.storage import get_last_signals
from ai_engine.multi_crawler import crawl


class BackfillEngine:

    def __init__(self):
        self.fallback_limit = 20

    def run(self):
        logger.info("[BACKFILL] triggered")

        # 1. retry live crawl first
        fresh = crawl()

        if fresh:
            logger.info("[BACKFILL] recovered from live crawl")
            return fresh

        # 2. fallback memory layer (controlled)
        historical = get_last_signals(limit=self.fallback_limit)

        logger.warning("[BACKFILL] using historical fallback layer")

        return historical or []
