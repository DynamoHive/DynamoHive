import time
from ai_engine.global_intelligence_engine import build_intelligence_index
from ai_engine.crawler_engine import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.topic_radar import detect_topics
from ai_engine.analytics_engine import analyse
from ai_engine.signal_detector import detect_signals
from ai_engine.intelligence_engine import generate_intelligence

from ai_engine.knowledge_graph import update_graph
from ai_engine.knowledge_map import update_map
from ai_engine.vector_memory import store_vector

from ai_engine.trust_engine import evaluate_trust

from ai_engine.auto_content_loop import generate_content

from backend.feed_engine import publish
from backend.topic_authority_engine import update_topic_authority

from distribution.distribution_engine import distribute

from ai_engine.growth_engine import evaluate_growth
from ai_engine.viral_engine import simulate_viral


CYCLE_TIME = 600


def run_cycle():
def run_cycle():
    print("DynamoHive cycle start")

    # 1 INTERNET CRAWL
    raw_data = crawl()

    if not raw_data:
        print("crawler returned no data")
        return

    # 2 DATA PIPELINE
    data = process_data(raw_data)

    # 3 TOPIC DETECTION
    topics = detect_topics(data)

    # 4 ANALYTICS
    analysis = analyse(data)

    # 5 SIGNAL DETECTION
    signals = detect_signals(analysis)

    # 6 INTELLIGENCE GENERATION
    intelligence = generate_intelligence(signals)

    # 7 TRUST EVALUATION
    trust_score = evaluate_trust(intelligence)

    if trust_score < 0.3:
        print("content rejected (low trust)")
        return

    # 8 KNOWLEDGE GRAPH UPDATE
    update_graph(intelligence)

    # 9 KNOWLEDGE MAP UPDATE
    update_map(intelligence)

    # 10 VECTOR MEMORY STORAGE
    store_vector(intelligence)

    # 11 CONTENT GENERATION
    post = generate_content(intelligence)

    if not post:
        print("no content generated")
        return

    # 12 TOPIC AUTHORITY UPDATE
    update_topic_authority(post["topic"])

    # 13 PUBLISH
    publish(post)

    # 14 DISTRIBUTION
    distribute(post)

    # 15 GROWTH ANALYSIS
    evaluate_growth(post)

    # 16 VIRAL SIMULATION
    simulate_viral(post)

    print("cycle complete")


def start():

    print("DynamoHive orchestrator started")

    while True:

        try:

            run_cycle()

        except Exception as e:

            print("orchestrator error:", e)

        time.sleep(CYCLE_TIME)
