import time
import gc
import traceback

from backend.logger import logger
from backend.storage import save_post, get_posts

# 🔥 EVENT ENGINE
from ai_engine.events import register_event, detect_event_spikes

# 🔥 CONTENT + DISTRIBUTION
from ai_engine.auto_content_loop import generate_content
from ai_engine.distribution_engine import distribute

CYCLE_INTERVAL = 30
ERROR_SLEEP = 30


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

        # 🔴 1. DATA
        raw_data = modules["crawl"]()
        previous_posts = get_posts()

        if not raw_data:
            if previous_posts:
                logger.warning("no new crawl data, using stored data")
                raw_data = previous_posts
            else:
                logger.warning("no crawl data at all")
                return

        # 🔴 2. PIPELINE
        if "process_data" in modules:
            raw_data = modules["process_data"](raw_data)

        # 🔴 3. TOPICS
        topics = modules["detect_topics"](raw_data) if "detect_topics" in modules else raw_data
        logger.info(f"topics detected: {topics}")

        # 🔴 4. ANALYTICS
        analytics = modules["analyse"](topics) if "analyse" in modules else topics

        # 🔴 5. SIGNALS
        signals = modules["detect_signals"](analytics) if "detect_signals" in modules else []
        logger.info(f"signals detected: {len(signals)}")

        # 🔴 6. EVENT MEMORY
        for signal in signals:
            for kw in signal.get("keywords", []):
                register_event(kw)

        # 🔴 7. EVENTS
        events = detect_event_spikes()
        logger.info(f"events detected: {len(events)}")

        # 🔴 8. CONTENT + DISTRIBUTION
        for event in events:
            try:
                content = generate_content(event)

                if content:
                    save_post(
                        f"Event: {event.get('topic')}",
                        content
                    )

                    distribute(content)

                    logger.info(f"content generated + distributed: {event.get('topic')}")

            except Exception as e:
                logger.warning(f"content/distribution error: {e}")

        # 🔴 9. RAW STORAGE
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
