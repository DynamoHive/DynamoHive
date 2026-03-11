import time

from backend.logger import logger
from ai_engine.event_engine import register_event, detect_event_spikes
from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.topic_radar import detect_topics
from ai_engine.analytics_engine import analyse
from ai_engine.signal_detector import detect_signals
from ai_engine.intelligence_engine import generate_intelligence
from ai_engine.auto_content_loop import generate_content

from ai_engine.knowledge_graph import update_graph
from ai_engine.topic_learning_engine import learn_topics
from ai_engine.vector_memory import store_vector

from ai_engine.trend_engine import update_trends
from ai_engine.viral_engine import detect_viral
from ai_engine.growth_engine import update_growth

from ai_engine.entity_extraction import extract_entities
from ai_engine.actor_network import update_actor_network
from ai_engine.propaganda_detector import detect_propaganda
from ai_engine.geopolitical_signals import detect_geopolitical_signal
from ai_engine.narrative_engine import update_narratives

from backend.feed_engine import publish
from backend.distribution_engine import distribute


CYCLE_TIME = 600


def run_cycle():

    logger.info("DynamoHive cycle start")

    raw_data = crawl()

    if not raw_data:
        logger.info("no crawl data")
        return

    data = process_data(raw_data)

    if not data:
        logger.info("pipeline empty")
        return

    topics = detect_topics(data)
for t in topics:
    register_event(t)
    update_trends(topics)

    viral_topics = detect_viral(topics)

    for t in topics:
        update_growth(t)

    analysis = analyse(data)
for t in topics:
    register_event(t)
    signals = detect_signals(analysis)

    if not signals:
        logger.info("no signals detected")
        return

    intelligence = generate_intelligence(signals)

    if not intelligence:
        logger.info("no intelligence")
        return

    # ---------------- AI ANALYSIS ----------------

    entities = extract_entities(intelligence["content"])

    update_actor_network(entities)

    propaganda = detect_propaganda(intelligence["content"])

    geo_signal = detect_geopolitical_signal(intelligence["content"])

    narratives = update_narratives(intelligence["content"], entities)

    logger.info(f"entities: {entities}")
    logger.info(f"propaganda score: {propaganda}")
    logger.info(f"geopolitical signal: {geo_signal}")
    logger.info(f"narratives: {narratives}")

    # ---------------- CONTENT ----------------

    post = generate_content(intelligence)

    if not post:
        logger.info("no content generated")
        return

    publish(post)

    update_graph(post)
    learn_topics(post)
    store_vector(post)

    distribute(post)

    logger.info("cycle complete")


def start():

    logger.info("DynamoHive orchestrator started")
    logger.info(f"cycle interval: {CYCLE_TIME}s")

    while True:

        cycle_start = time.time()

        try:
            run_cycle()

        except Exception as e:
            logger.error(f"orchestrator error: {e}")

        elapsed = time.time() - cycle_start

        sleep_time = max(0, CYCLE_TIME - elapsed)

        time.sleep(sleep_time)
