import time
from backend.auto_content_loop import run_content_loop
from backend.data_pipeline import start_pipeline
from backend.growth_engine import start_growth
from backend.viral_engine import start_viral_engine
from backend.knowledge_ai import run_ai_analysis
from backend.knowledge_graph import update_graph

class DynamoHiveCore:

    def start(self):

        start_pipeline()
        start_growth()
        start_viral_engine()

        while True:
            time.sleep(30)
