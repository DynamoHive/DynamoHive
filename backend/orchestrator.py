import time
import gc
from concurrent.futures import ThreadPoolExecutor

from backend.logger import logger

CYCLE_INTERVAL = 30
ERROR_SLEEP = 30
MAX_WORKERS = 4


def safe_imports():

    modules = {}

    try:
        from backend.ai_engine.multi_crawler import crawl
        modules["crawl"] = crawl
        logger.info("crawler loaded")
    except Exception as e:
        logger.error(f"crawler import failed: {e}")

    try:
        from backend.ai_engine.data_pipeline import process_data
        modules["process_data"] = process_data
        logger.info("pipeline loaded")
    except Exception as e:
        logger.error(f"pipeline import failed: {e}")

    try:
        from backend.ai_engine.topic_radar import detect_topics
        modules["detect_topics"] = detect_topics
        logger.info("topic radar loaded")
    except Exception as e:
        logger.error(f"topic radar import failed: {e}")

    try:
        from backend.ai_engine.analytics_engine import analyse
        modules["analyse"] = analyse
        logger.info("analytics loaded")
    except Exception as e:
        logger.error(f"analytics import failed: {e}")

    try:
        from backend.ai_engine.signal_detector import detect_signals
        modules["detect_signals"] = detect_signals
        logger.info("signal detector loaded")
    except Exception as e:
        logger.error(f"signal detector import failed: {e}")

    return modules


def run_cycle(modules):

    start_time = time.time()
    logger.info("DynamoHive cycle started")

    try:

        if "crawl" not in modules:
            logger.warning("crawler missing")
            return

        raw_data = modules["crawl"]()

        if not raw_data:
            logger.warning("no crawl data")
            return

        if "process_data" in modules:
            raw_data = modules["process_data"](raw_data)

        if "detect_topics" in modules:
            topics = modules["detect_topics"](raw_data)
        else:
            topics = raw_data

        if "analyse" in modules:
            analytics = modules["analyse"](topics)
        else:
            analytics = topics

        if "detect_signals" in modules:
            signals = modules["detect_signals"](analytics)
        else:
            signals = []

        logger.info(f"signals detected: {len(signals)}")

    except Exception as e:
        logger.error(f"cycle error: {e}")

    finally:
        gc.collect()
        elapsed = round(time.time() - start_time, 2)
        logger.info(f"cycle finished in {elapsed}s")


def start():

    logger.info("DynamoHive system started")

    modules = safe_imports()

    while True:

        try:

            run_cycle(modules)
            time.sleep(CYCLE_INTERVAL)

        except Exception as e:

            logger.error(f"system error: {e}")
            time.sleep(ERROR_SLEEP)
