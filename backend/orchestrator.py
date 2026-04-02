import time
import gc
import traceback

from backend.logger import logger
from backend.storage import save_post, get_posts

from ai_engine.event_engine import register_event, detect_event_spikes
from ai_engine.narrative_engine import generate_narrative
from backend.distribution_engine import distribute

import ai_engine.signal_detector as signal_module
from ai_engine.signal_ranking_engine import rank_signals

from backend.cache import is_duplicate, mark_generated
from ai_engine.global_intelligence_engine import GlobalIntelligenceEngine


intel_engine = GlobalIntelligenceEngine()

CYCLE_INTERVAL = 30
ERROR_SLEEP = 30


def synthesize_intelligence(signals, events):

    intelligence = []

    for s in signals:
        topic = s.get("text") or "unknown"

        intelligence.append({
            "topic": topic,
            "summary": f"{topic} shows emerging structural signals in global systems.",
            "trend": "surging" if s.get("score", 0) > 3 else "rising"
        })

    return intelligence


def safe_imports():

    modules = {}

    try:
        from ai_engine.multi_crawler import crawl
        modules["crawl"] = crawl
    except Exception:
        traceback.print_exc()

    try:
        from ai_engine.data_pipeline import process_data
        modules["process_data"] = process_data
    except Exception:
        traceback.print_exc()

    return modules


def run_cycle(modules):

    start_time = time.time()
    logger.info("DynamoHive cycle started")

    try:

        # ilk post garanti
        if not get_posts():
            save_post("DynamoHive Activated", "System is live")

        raw_data = modules.get("crawl", lambda: [])()
        previous_posts = get_posts()

        if not raw_data:
            raw_data = previous_posts or [{"text": "bootstrap"}]

        if "process_data" in modules:
            raw_data = modules["process_data"](raw_data)

        # SIGNAL
        signals = signal_module.detect_signals(raw_data) if raw_data else []

        if not signals:
            signals = [{
                "text": f"system_{int(time.time())}",
                "score": 1
            }]

        signals = rank_signals(signals)

        # EVENTS
        for signal in signals:
            register_event(signal.get("text"))

        events = detect_event_spikes()

        # BASE INTEL
        raw_intel = synthesize_intelligence(signals, events)

        # INTELLIGENCE
        try:
            intelligence = intel_engine.process(raw_intel)
        except Exception as e:
            print("INTEL ERROR:", e)
            intelligence = raw_intel

        # CONTENT
        for intel in intelligence:

            base_topic = intel.get("topic") or "unknown"

            # duplicate sistemi kilitlemez
            if is_duplicate(base_topic):
                topic = f"{base_topic}_{int(time.time())}"
            else:
                topic = base_topic

            content = generate_narrative(intel)

            if not content:
                continue

            title = content.get("title") or topic
            body = content.get("content") or "No content"

            save_post(title, body)

            try:
                distribute(content)
            except Exception:
                logger.warning("Distribution failed")

            mark_generated(topic)

            logger.info(f"GENERATED: {topic}")

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
🔥 BU VERSİYONDA     
