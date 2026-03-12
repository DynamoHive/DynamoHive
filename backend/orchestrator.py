import time
import gc

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
from ai_engine.trend_scoring_engine import is_trending

from ai_engine.source_intelligence import SourceIntelligence
from ai_engine.signal_ranking_engine import rank_signals
from ai_engine.memory_pattern_engine import MemoryPatternEngine


CYCLE_INTERVAL = 600
ERROR_SLEEP = 30


source_intel = SourceIntelligence()
memory_engine = MemoryPatternEngine()


def run_cycle():

    start_time = time.time()

    logger.info("DynamoHive cycle started")

    try:

        raw_data = crawl()

        if not raw_data:
            logger.warning("No data from crawler")
            return

        processed = process_data(raw_data)

        if not processed:
            logger.warning("Pipeline returned empty data")
            return

        topics = detect_topics(processed)

        if not topics:
            logger.warning("No topics detected")
            return

        analytics = analyse(topics) or {}

        signals = detect_signals(analytics)

        if not signals:
            logger.info("No signals detected")
            return

        signals = rank_signals(signals)

        signals = [s for s in signals if not memory_engine.seen_before(s)]

        if not signals:
            logger.info("Signals filtered by memory engine")
            return

        for s in signals:
            memory_engine.store(s)

        intelligence = generate_intelligence(signals)

        if not intelligence:
            logger.info("No intelligence generated")
            return

        update_graph(intelligence)

        learn_topics(intelligence)

        if is_trending(intelligence):

            generate_content(intelligence)

            logger.info("Trending content generated")

        else:

            logger.info("Topic skipped (not trending)")

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
