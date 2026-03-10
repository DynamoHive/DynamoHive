import time
import backend.intelligence_engine as intelligence_engine
from backend.data_pipeline import start_pipeline
from backend.growth_engine import start_growth
from backend.viral_engine import start_viral_engine
import backend.crawler_engine as crawler_engine
import backend.topic_radar as topic_radar
import backend.analytics_engine as analytics_engine
import backend.auto_content_loop as auto_content_loop
import backend.feed_engine as feed_engine
import backend.knowledge_ai as knowledge_ai
import backend.knowledge_graph as knowledge_graph
import backend.knowledge_map as knowledge_map
import backend.trend_engine as trend_engine
import backend.signal_detector as signal_detector
import backend.crawler_engine as crawler_engine 
import backend.vector_memory as vector_memory
def safe_run(module):
    try:
        if hasattr(module, "run"):
            module.run()
        elif hasattr(module, "start"):
            module.start()
    except Exception as e:
        print("Module error:", module.__name__, e)


class DynamoHiveCore:

    def start(self):

        start_pipeline()
        start_growth()
        start_viral_engine()

        while True:safe_run(trend_engine)
            safe_run(crawler_engine)
        safe_run(intelligence_engine)
        safe_run(vector_memory)
safe_run(signal_detector)
safe_run(trend_engine)
safe_run(signal_detector)
            safe_run(topic_radar)
            safe_run(analytics_engine)

            safe_run(knowledge_ai)
            safe_run(knowledge_graph)
            safe_run(knowledge_map)

            safe_run(auto_content_loop)
            safe_run(feed_engine)

            time.sleep(30)
