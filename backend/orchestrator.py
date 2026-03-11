import time

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

from backend.feed_engine import publish
from backend.distribution_engine import distribute

CYCLE_TIME = 600


def run_cycle():

    print("DynamoHive cycle start")

    # 1️⃣ crawl
    raw_data = crawl()

    if not raw_data:
        print("no crawl data")
        return

    # 2️⃣ pipeline
    data = process_data(raw_data)

    if not data:
        print("pipeline empty")
        return

    # 3️⃣ topic detection
    topics = detect_topics(data)

    # 4️⃣ analytics
    analysis = analyse(data)

    # 5️⃣ signal detection
    signals = detect_signals(analysis)

    # 6️⃣ intelligence
    intelligence = generate_intelligence(signals)

    if not intelligence:
        print("no intelligence")
        return

    # 7️⃣ content generation
    post = generate_content(intelligence)

    if not post:
        print("no content generated")
        return

    # 8️⃣ publish
    publish(post)

    # 9️⃣ knowledge systems
    update_graph(post)
    learn_topics(post)
    store_vector(post)

    # 🔟 distribution
    distribute(post)

 logger.error(f"orchestrator error: {e}")


def start():

    logger.info("DynamoHive cycle start")

    while True:

        try:
            run_cycle()

        except Exception as e:
            print("orchestrator error:", e)

        time.sleep(CYCLE_TIME)
