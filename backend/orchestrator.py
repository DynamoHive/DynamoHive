import time
import gc

from backend.logger import logger

from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.topic_radar import detect_topics
from ai_engine.analytics_engine import analyse
from ai_engine.signal_detector import detect_signals
from ai_engine.global_intelligence_engine import generate_intelligence
from ai_engine.knowledge_graph import update_graph
from ai_engine.topic_learning_engine import learn_topics
from ai_engine.trend_scoring_engine import is_trending

from ai_engine.signal_ranking_engine import rank_signals
from ai_engine.memory_pattern_engine import MemoryPatternEngine

# newsroom layer
from backend.newsroom.story_engine import build_story
from backend.newsroom.editorial_engine import apply_editorial
from backend.newsroom.article_engine import generate_article
from backend.newsroom.publish_engine import publish_article


CYCLE_INTERVAL = 600
ERROR_SLEEP = 30

memory_engine = MemoryPatternEngine()


def run_cycle():

    start_time = time.time()

    logger.info("DynamoHive cycle started")

    try:

        # crawl data
        raw_data = crawl()

        if not raw_data:
            logger.warning("No data from crawler")
            return

        # pipeline processing
        processed = process_data(raw_data)

        if not processed:
            logger.warning("Pipeline returned empty data")
            return

        # topic detection
        topics = detect_topics(processed)

        if not topics:
            logger.warning("No topics detected")
            return

        # analytics
        analytics = analyse(topics) or {}

        # signal detection
        signals = detect_signals(analytics)

        if not signals:
            logger.info("No signals detected")
            return

        # ranking
        signals = rank_signals(signals)

        # memory filtering
        new_signals = []

        for s in signals:
            if not memory_engine.seen_before(s):
                memory_engine.store(s)
                new_signals.append(s)

        if not new_signals:
            logger.info("Signals filtered by memory engine")
            return

        # intelligence generation
        intelligence = generate_intelligence(new_signals)

        if not intelligence:
            logger.info("No intelligence generated")
            return

        # knowledge graph update
        update_graph(intelligence)

        # topic learning
        learn_topics(intelligence)

        # trend check
        if not is_trending(intelligence):
            logger.info("Topic skipped (not trending)")
            return

        # newsroom pipeline
        story = build_story(intelligence)

        story = apply_editorial(story)

        article = generate_article(story)

        publish_article(article)

        logger.info("Intelligence article published")

    except Exception as e:

        logger.error(f"Cycle error: {e}")

    finally:

        gc.collect()

        elapsed = round(time.time() - start_time, 2)

        logger.info(f"Cycle finished in {elapsed}s")


def start():

    logger.info("DynamoHive system started")

    while True:

        try:

            run_cycle()

            time.sleep(CYCLE_INTERVAL)

        except Exception as e:

            logger.error(f"System error: {e}")

            time.sleep(ERROR_SLEEP)

          
