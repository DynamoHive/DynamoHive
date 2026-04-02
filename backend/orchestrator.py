import time
import gc
import traceback

from backend.logger import logger
from backend.storage import save_post, get_posts

# ✅ DOĞRU IMPORTLAR
from ai_engine.event_engine import register_event, detect_event_spikes
from backend.distribution_engine import distribute
from ai_engine.auto_content_loop import generate_content

import ai_engine.signal_detector as signal_module
from ai_engine.signal_ranking_engine import rank_signals

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

    return modules


def run_cycle(modules):

    start_time = time.time()
    logger.info("DynamoHive cycle started")

    try:

        if "crawl" not in modules:
            logger.warning("crawler missing")
            return

        # 🔴 DATA
        raw_data = modules["crawl"]()
        previous_posts = get_posts()

        if not raw_data:
            if previous_posts:
                logger.warning("no new crawl data, using stored data")
                raw_data = previous_posts
            else:
                logger.warning("no crawl data at all")
                return

        # 🔴 PIPELINE
        if "process_data" in modules:
            raw_data = modules["process_data"](raw_data)

        # 🔴 TOPICS
        topics = modules["detect_topics"](raw_data) if "detect_topics" in modules else raw_data
        logger.info(f"topics detected: {topics}")

        # 🔴 ANALYTICS
        analytics = modules["analyse"](topics) if "analyse" in modules else topics

        # 🔥 SIGNALS
        signals = signal_module.detect_signals(analytics) if analytics else []

        # 🔥 FALLBACK
        if not signals and topics:
            logger.warning("no signals → fallback to topics")
            signals = [
                {
                    "text": t.get("topic"),
                    "keywords": [t.get("topic")],
                    "score": t.get("score", 0)
                }
                for t in topics if isinstance(t, dict)
            ]

        # 🔥 RANKING
        signals = rank_signals(signals)

        logger.info(f"signals detected: {len(signals)}")
        logger.info(f"SIGNAL SAMPLE: {signals[:1]}")

        # 🔴 EVENT MEMORY
        for signal in signals:
            keywords = signal.get("keywords") or [signal.get("text")]
            for kw in keywords:
                if kw:
                    register_event(kw)

        # 🔴 EVENTS
        events = detect_event_spikes()
        logger.info(f"events detected: {len(events)}")

        # 🔴 CONTENT + DISTRIBUTION (🔥 TAM FIX)
        for event in events:
            try:
                content = generate_content(event)

                if not content:
                    continue

                # 🔥 NORMALIZE
                if isinstance(content, dict):
                    title = content.get("title", f"Event: {event.get('topic')}")
                    body = content.get("content", "")
                else:
                    title = f"Event: {event.get('topic')}"
                    body = str(content)

                # 🔴 DATABASE (STRING ONLY)
                save_post(title, body)

                # 🔴 DISTRIBUTION (STANDARD FORMAT)
                distribute({
                    "title": title,
                    "content": body
                })

                logger.info(f"content generated + distributed: {event.get('topic')}")

            except Exception as e:
                logger.warning(f"content/distribution error: {e}")

        # 🔴 STORAGE (RAW DATA)
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
