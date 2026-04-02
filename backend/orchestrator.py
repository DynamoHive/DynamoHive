import time
import gc
import traceback
from concurrent.futures import ThreadPoolExecutor

from backend.logger import logger
from backend.storage import save_post, get_posts

CYCLE_INTERVAL = 30
ERROR_SLEEP = 30
MAX_WORKERS = 4


def safe_imports():

    modules = {}

    try:
        from ai_engine.multi_crawler import crawl
        modules["crawl"] = crawl
        logger.info("crawler loaded")
    except Exception:
        traceback.print_exc()

    try:
        from ai_engine.data_pipeline import process_data
        modules["process_data"] = process_data
        logger.info("pipeline loaded")
    except Exception:
        traceback.print_exc()

    try:
        from ai_engine.topic_radar import detect_topics
        modules["detect_topics"] = detect_topics
        logger.info("topic radar loaded")
    except Exception:
        traceback.print_exc()

    try:
        from ai_engine.analytics_engine import analyse
        modules["analyse"] = analyse
        logger.info("analytics loaded")
    except Exception:
        traceback.print_exc()

    try:
        from ai_engine.signal_detector import detect_signals
        modules["detect_signals"] = detect_signals
        logger.info("signal detector loaded")
    except Exception:
        traceback.print_exc()

    return modules


def run_cycle(modules):

    start_time = time.time()
    logger.info("DynamoHive cycle started")

    try:

        if "crawl" not in modules:
            logger.warning("crawler missing")
            return

        # 🔴 1. yeni veri çek
        raw_data = modules["crawl"]()

        # 🔴 2. geçmiş veriyi al
        previous_posts = get_posts()

        # 🔴 3. fallback mekanizması
        if not raw_data:
            if previous_posts:
                logger.warning("no new crawl data, using stored data")
                raw_data = previous_posts
            else:
                logger.warning("no crawl data at all")
                return

        # 🔴 4. pipeline
        if "process_data" in modules:
            raw_data = modules["process_data"](raw_data)

        # 🔴 5. topic detection
        if "detect_topics" in modules:
            topics = modules["detect_topics"](raw_data)
        else:
            topics = raw_data

        logger.info(f"topics detected: {topics}")

        # 🔴 6. analytics
        if "analyse" in modules:
            analytics = modules["analyse"](topics)
        else:
            analytics = topics

        # 🔴 7. signal detection
        if "detect_signals" in modules:
            signals = modules["detect_signals"](analytics)
        else:
            signals = []

        logger.info(f"signals detected: {len(signals)}")

        # 🔴 8. veriyi kaydet (memory)
        try:
            for item in raw_data:
                if isinstance(item, dict):
                    save_post(
                        item.get("title", ""),
                        item.get("content", "")
                    )
        except Exception as e:
            logger.warning(f"storage error: {e}")

    except Exception:
        traceback.print_exc()

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

        except Exception:
            traceback.print_exc()
            time.sleep(ERROR_SLEEP)
