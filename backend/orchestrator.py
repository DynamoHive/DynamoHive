import time
import gc
from concurrent.futures import ThreadPoolExecutor

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

# newsroom
from backend.newsroom.story_engine import build_story
from backend.newsroom.editorial_engine import apply_editorial
from backend.newsroom.article_engine import generate_article
from backend.newsroom.publish_engine import publish_article


CYCLE_INTERVAL = 600
ERROR_SLEEP = 30
MAX_WORKERS = 4

memory_engine = MemoryPatternEngine()


def parallel_crawl():

    logger.info("Starting parallel crawl")

    try:

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

            future = executor.submit(crawl)

            data = future.result()

        return data or []

    except Exception as e:

        logger.error(f"Crawl failed: {e}")

        return []


def newsroom_pipeline(intel):

    try:

        if not is_trending(intel):

            logger.info("Signal skipped (not trending)")

            return False

        story = build_story(intel)

        story = apply_editorial(story)

        article = generate_article(story)

        publish_article(article)

        logger.info("Article published")

        return True

    except Exception as e:

        logger.warning(f"Newsroom error: {e}")

        return False


def run_cycle():

    start_time = time.time()

    stats = {
        "raw": 0,
        "processed": 0,
        "topics": 0,
        "signals": 0,
        "published": 0
    }

    logger.info("DynamoHive cycle started")

    try:

        # 1️⃣ Crawl
        raw_data = parallel_crawl()

        stats["raw"] = len(raw_data)

        if not raw_data:
            logger.warning("No crawl data")
            return

        # 2️⃣ Pipeline
        processed = process_data(raw_data) or []

        stats["processed"] = len(processed)

        if not processed:
            logger.warning("No processed data")
            return

        # 3️⃣ Topics
        topics = detect_topics(processed) or []

        stats["topics"] = len(topics)

        if not topics:
            logger.warning("No topics detected")
            return

        # 4️⃣ Analytics
        analytics = analyse(topics) or {}

        # 5️⃣ Signals
        signals = detect_signals(analytics) or []

        if not signals:
            logger.info("No signals detected")
            return

        # 6️⃣ Ranking
        signals = rank_signals(signals)

        stats["signals"] = len(signals)

        # 7️⃣ Memory filter
        new_signals = []

        for s in signals:

            if not memory_engine.seen_before(s):

                memory_engine.store(s)

                new_signals.append(s)

        if not new_signals:
            logger.info("All signals filtered by memory")
            return

        # 8️⃣ Intelligence
        intelligence = generate_intelligence(new_signals)

        if not intelligence:
            logger.info("No intelligence generated")
            return

        if not isinstance(intelligence, list):
            intelligence = [intelligence]

        # 9️⃣ Graph update
        try:
            update_graph(intelligence)
        except Exception as e:
            logger.warning(f"Graph update failed: {e}")

        # 🔟 Learning
        try:
            learn_topics(intelligence)
        except Exception as e:
            logger.warning(f"Learning failed: {e}")

        # 11️⃣ Newsroom publishing
        published = 0

        for intel in intelligence:

            if newsroom_pipeline(intel):
                published += 1

        stats["published"] = published

        logger.info(f"Articles published: {published}")

    except Exception as e:

        logger.error(f"Cycle error: {e}")

    finally:

        gc.collect()

        elapsed = round(time.time() - start_time, 2)

        logger.info(
            f"Cycle finished in {elapsed}s | "
            f"raw:{stats['raw']} "
            f"processed:{stats['processed']} "
            f"topics:{stats['topics']} "
            f"signals:{stats['signals']} "
            f"published:{stats['published']}"
        )


def start():

    logger.info("DynamoHive system started")

    while True:

        try:

            run_cycle()

            time.sleep(CYCLE_INTERVAL)

        except Exception as e:

            logger.error(f"System error: {e}")

            time.sleep(ERROR_SLEEP)

          
