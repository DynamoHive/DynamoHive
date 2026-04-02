import time
import gc
import traceback

from backend.logger import logger
from backend.storage import save_post, get_posts

# EVENT
from ai_engine.event_engine import register_event, detect_event_spikes

# CONTENT
from ai_engine.narrative_engine import generate_narrative

# DISTRIBUTION
from backend.distribution_engine import distribute

# SIGNAL
import ai_engine.signal_detector as signal_module
from ai_engine.signal_ranking_engine import rank_signals

# CACHE
from backend.cache import is_duplicate, mark_generated


CYCLE_INTERVAL = 30
ERROR_SLEEP = 30


# INTELLIGENCE (yerinde, basit ve çalışır)
def synthesize_intelligence(signals, events):
    intelligence = []
    for s in signals:
        topic = s.get("text") or "unknown"
        intelligence.append({
            "topic": topic,
            "summary": f"{topic} is gaining momentum based on detected signals.",
            "trend": "surging" if s.get("score", 0) > 5 else "rising"
        })
    return intelligence


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
        # 1) DATA
        raw_data = modules.get("crawl", lambda: [])()
        previous_posts = get_posts()

        if not raw_data:
            if previous_posts:
                logger.warning("no new crawl data, using stored data")
                raw_data = previous_posts
            else:
                logger.warning("no crawl data at all → continue anyway")

        # 2) PIPELINE
        if "process_data" in modules:
            raw_data = modules["process_data"](raw_data)

        # 3) TOPICS
        topics = modules.get("detect_topics", lambda x: x)(raw_data)

        # 4) ANALYTICS
        analytics = modules.get("analyse", lambda x: x)(topics)

        # 5) SIGNALS
        signals = signal_module.detect_signals(analytics) if analytics else []

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

        signals = rank_signals(signals)

        # 💣 GARANTİ TETİKLEME (KRİTİK)
        if not signals:
            logger.warning("FORCE SIGNAL ACTIVATED")
            signals = [{
                "text": "system activation",
                "keywords": ["system"],
                "score": 10
            }]

        logger.info(f"signals detected: {len(signals)}")

        # 6) EVENTS
        for signal in signals:
            kws = signal.get("keywords") or [signal.get("text")]
            for kw in kws:
                if kw:
                    register_event(kw)

        events = detect_event_spikes()

        # 7) INTELLIGENCE
        intelligence = synthesize_intelligence(signals, events)
        logger.info(f"intelligence generated: {len(intelligence)}")

        # 8) CONTENT + DISTRIBUTION
        for intel in intelligence:
            topic = intel.get("topic")

            if is_duplicate(topic):
                logger.info(f"duplicate skipped: {topic}")
                continue

            try:
                content = generate_narrative(intel)

                if isinstance(content, dict):
                    title = content.get("title", f"Intel: {topic}")
                    body = content.get("content", "")

                    save_post(title, body)
                    distribute(content)
                    mark_generated(topic)

                    logger.info(f"GENERATED: {topic}")
                else:
                    logger.warning("invalid content format")

            except Exception as e:
                logger.warning(f"intel error: {e}")

        # 9) RAW STORAGE (opsiyonel)
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
