import time

from backend.logger import logger

from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.topic_radar import detect_topics
from ai_engine.analytics_engine import analyse
from ai_engine.signal_detector import detect_signals
from ai_engine.intelligence_engine import generate_intelligence
from ai_engine.auto_content_loop import generate_content
from ai_engine.topic_authority_engine import update_topic_authority
from ai_engine.knowledge_graph import update_graph
from ai_engine.topic_learning_engine import learn_topics
from ai_engine.vector_memory import store_vector

from backend.feed_engine import publish
from backend.distribution_engine import distribute


CYCLE_TIME = 600


def run_cycle():

    logger.info("DynamoHive cycle start")

    try:

        raw_data = crawl()

        if not raw_data:
            logger.info("no crawl data")
            return

        data = process_data(raw_data)

        if not data:
            logger.info("pipeline empty")
            return

        topics = detect_topics(data)
update_topic_authority(topics)
        analysis = analyse(data)

        signals = detect_signals(analysis)

        if not signals:
            logger.info("no signals detected")
            return

        intelligence = generate_intelligence(signals)

        if not intelligence:
            logger.info("no intelligence")
            return

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

    except Exception as e:

        logger.error(f"cycle error: {e}")


def start():

    logger.info("DynamoHive orchestrator started")

    while True:

        try:

            run_cycle()

        except Exception as e:

            logger.error(f"orchestrator error: {e}")

        finally:

            time.sleep(CYCLE_TIME)
