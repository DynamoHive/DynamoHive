import time
from ai_engine.vector_memory import store_vector
from ai_engine.crawler_engine import crawl
from ai_engine.topic_radar import detect_topics
from ai_engine.analytics_engine import analyse
from ai_engine.signal_detector import detect_signals
from ai_engine.intelligence_engine import generate_intelligence
from ai_engine.auto_content_loop import generate_content
from ai_engine.data_pipeline import process_data
from backend.feed_engine import publish
from ai_engine.topic_learning_engine import learn_topics
from ai_engine.knowledge_graph import update_graph
CYCLE_TIME = 600


def run_cycle():publish(post)
update_graph(post)
    print("DynamoHive cycle start")

    data = crawl()
data = process_data(raw_data)
    if not data:
        print("no crawl data")
        return

    topics = detect_topics(data)

    analysis = analyse(data)

    signals = detect_signals(analysis)

    intelligence = generate_intelligence(signals)

    post = generate_content(intelligence)

    if not post:
        print("no content generated")
        return

    publish(post)

    print("cycle complete")


def start():

    print("DynamoHive orchestrator started")

    while True:

        try:
            run_cycle()

        except Exception as e:
            print("orchestrator error:", e)

        time.sleep(CYCLE_TIME)
