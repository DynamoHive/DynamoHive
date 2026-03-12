import time
from backend.logger import logger

# AI ENGINE MODULES
from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.topic_radar import detect_topics
from ai_engine.analytics_engine import analyse
from ai_engine.signal_detector import detect_signals
from ai_engine.intelligence_engine import generate_intelligence
from ai_engine.auto_content_loop import generate_content
from ai_engine.knowledge_graph import update_graph
from ai_engine.topic_learning_engine import learn_topics
from ai_engine.trend_scoring_engine import is_trending


CYCLE_INTERVAL = 600  # 10 dakika


def run_cycle():

    logger.info("DynamoHive cycle started")

    try:

        # 1 CRAWL
        raw_data = crawl()

        if not raw_data:
            logger.warning("Crawler returned no data")
            return

        # 2 DATA PIPELINE
        processed_data = process_data(raw_data)

        if not processed_data:
            logger.warning("Data pipeline returned empty result")
            return

        # 3 TOPIC DETECTION
        topics = detect_topics(processed_data)

        # 4 ANALYTICS
        analytics = analyse(topics)

        # 5 SIGNAL DETECTION
        signals = detect_signals(analytics)

        # 6 INTELLIGENCE
        intelligence = generate_intelligence(signals)

        # 7 KNOWLEDGE GRAPH
        update_graph(intelligence)

        # 8 LEARNING
        learn_topics(intelligence)

        # 9 TREND FILTER + CONTENT
        if is_trending(intelligence):

            generate_content(intelligence)

            logger.info("Content generated for trending topic")

        else:

            logger.info("Topic not strong enough for content")

        logger.info("Cycle completed")

    except Exception as e:

        logger.error(f"DynamoHive cycle error: {e}")


def start():

    logger.info("DynamoHive system started")

    while True:

        run_cycle()

        time.sleep(CYCLE_INTERVAL)


if __name__ == "__main__":

    start()
