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


# INTELLIGENCE
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
    except:
        traceback.print_exc()

    try:
        from ai_engine.data_pipeline import process_data
        modules["process_data"] = process_data
    except:
        traceback.print_exc()

    try:
        from ai_engine.topic_radar import detect_topics
        modules["detect_topics"] = detect_topics
    except:
        traceback.print_exc()

    try:
        from ai_engine.analytics_engine import analyse
        modules["analyse"] = analyse
    except:
        traceback.print_exc()

    return modules


def run_cycle(modules):

    start_time = time.time()
    logger.info("DynamoHive cycle started")

    try:
        # 💣 TEST POST (GARANTİ)
        save_post("TEST TITLE", "SYSTEM WORKING")

        # DATA
        raw_data = modules.get("crawl", lambda: [])()
        previous_posts = get_posts()

        if not raw_data:
            raw_data = previous_posts or []

        # PIPELINE
        if "process_data" in modules:
            raw_data = modules["process_data"](raw_data)

        # TOPICS
        topics = modules.get("detect_topics", lambda x: x)(raw_data)

        # ANALYTICS
        analytics = modules.get("analyse", lambda x: x)(topics)

        # SIGNALS
        signals = signal_module.detect_signals(analytics) if analytics else []

        if not signals:
            signals = [{
                "text": "system activation",
                "score": 10
            }]

        signals = rank_signals(signals)

        # EVENTS
        for signal in signals:
            register_event(signal.get("text"))

        events = detect_event_spikes()

        # INTELLIGENCE
        intelligence = synthesize_intelligence(signals, events)

        # CONTENT
        for intel in intelligence:

            topic = intel.get("topic")

            if is_duplicate(topic):
                continue

            content = generate_narrative(intel)

            if isinstance(content, dict):

                save_post(
                    content.get("title"),
                    content.get("content")
                )

                distribute(content)
                mark_generated(topic)

    except:
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
        except:
            traceback.print_exc()
            time.sleep(ERROR_SLEEP)
