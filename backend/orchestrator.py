import time

from backend.data_pipeline import start_pipeline
from backend.growth_engine import start_growth
from backend.viral_engine import start_viral_engine

import backend.topic_radar
import backend.analytics_engine
import backend.auto_content_loop
import backend.feed_engine
import backend.knowledge_ai
import backend.knowledge_graph


class DynamoHiveCore:

    def start(self):

        start_pipeline()
        start_growth()
        start_viral_engine()

        while True:

            try:
                backend.topic_radar.run()
            except:
                pass

            try:
                backend.analytics_engine.run()
            except:
                pass

            try:
                backend.knowledge_ai.run()
            except:
                pass

            try:
                backend.knowledge_graph.run()
            except:
                pass

            try:
                backend.auto_content_loop.run()
            except:
                pass

            try:
                backend.feed_engine.run()
            except:
                pass

            time.sleep(30)
