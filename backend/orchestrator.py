import time
from backend.logger import logger

from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.topic_radar import detect_topics
from ai_engine.analytics_engine import analyse
from ai_engine.signal_detector import detect_signals
from ai_engine.intelligence_engine import generate_intelligence
from ai_engine.auto_content_loop import generate_content

from ai_engine.knowledge_graph import update_graph
from ai_engine.topic_learning_engine import learn_topics


CYCLE_INTERVAL = 600


def run_cycle():

    logger.info("DynamoHive cycle started")

    try:

        raw_data = crawl()
        if not raw_data:
            logger.warning("Crawler returned no data")
            return

        processed_data = process_data(raw_data)
        if not processed_data:
            logger.warning("Data pipeline produced empty output")
            return

        topics = detect_topics(processed_data)
        analytics = analyse(topics)
        signals = detect_signals(analytics)

        intelligence = generate_intelligence(signals)

        update_graph(intelligence)
        learn_topics(intelligence)

        generate_content(intelligence)

        logger.info("Cycle completed")

    except Exception as e:

        logger.error(f"Cycle failure: {e}")


def start():

    logger.info("DynamoHive system started")

    while True:

        run_cycle()

        time.sleep(CYCLE_INTERVAL)


if __name__ == "__main__":
    start()
Şu anda orchestrator ne yapıyor?
