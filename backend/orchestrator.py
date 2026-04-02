import time
import gc
import traceback
from collections import Counter

from backend.logger import logger
from backend.storage import save_post, get_posts

from ai_engine.event_engine import register_event, detect_event_spikes
from ai_engine.narrative_engine import generate_narrative
from backend.distribution_engine import distribute

import ai_engine.signal_detector as signal_module
from ai_engine.signal_ranking_engine import rank_signals

from backend.cache import is_duplicate, mark_generated


CYCLE_INTERVAL = 30
ERROR_SLEEP = 30


# 🔥 YENİ: TOPIC CLUSTERING
def extract_topics(raw_data):

    texts = []

    for item in raw_data:
        if isinstance(item, dict):
            text = item.get("title") or item.get("text") or ""
        else:
            text = str(item)

        if text:
            texts.append(text.lower())

    words = []
    for t in texts:
        words.extend(t.split())

    # basit filtre
    stopwords = {"the", "and", "is", "to", "of", "in", "on", "for", "with"}
    words = [w for w in words if w not in stopwords and len(w) > 3]

    counts = Counter(words)

    topics = []
    for word, count in counts.most_common(5):
        topics.append({
            "text": word,
            "score": count
        })

    return topics


def synthesize_intelligence(signals, events):

    intelligence = []

    for s in signals:
        topic = s.get("text") or "unknown"

        intelligence.append({
            "topic": topic,
            "summary": f"Recent developments around {topic} indicate structural shifts in global dynamics, supported by multiple emerging signals.",
            "trend": "surging" if s.get("score", 0) > 3 else "rising"
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

    return modules


def run_cycle(modules):

    start_time = time.time()
    logger.info("DynamoHive cycle started")

    try:

        # ilk post
        if not get_posts():
            save_post("DynamoHive Activated", "System is live and analyzing real-world signals")

        # DATA
        raw_data = modules.get("crawl", lambda: [])()
        previous_posts = get_posts()

        if not raw_data:
            raw_data = previous_posts or [{"text": "system bootstrap"}]

        if "process_data" in modules:
            raw_data = modules["process_data"](raw_data)

        # 🔥 YENİ: gerçek topic extraction
        signals = extract_topics(raw_data)

        # fallback
        if not signals:
            signals = [{
                "text": f"system {int(time.time())}",
                "score": 1
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

            topic = intel.get("topic") or f"unknown-{int(time.time())}"

            if is_duplicate(topic):
                logger.info(f"SKIPPED duplicate: {topic}")
                continue

            content = generate_narrative(intel)

            if not content:
                continue

            title = content.get("title") or topic
            body = content.get("content") or "No content"

            save_post(title, body)

            try:
                distribute(content)
            except:
                logger.warning("Distribution failed")

            mark_generated(topic)

            logger.info(f"GENERATED: {topic}")

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
