import time
import traceback

from backend.logger import logger

# ENGINE IMPORTS
from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.signal_detector import detect_signals

from ai_engine.intelligence.enrich_intelligence import enrich_intelligence
from ai_engine.intelligence.decision_engine import should_generate
from ai_engine.intelligence.memory_engine import MemoryEngine
from ai_engine.intelligence.learning_pipeline import LearningPipeline


# INIT SYSTEMS
memory = MemoryEngine()

WEIGHTS = {
    "geopolitical escalation": 2.5,
    "system instability": 1.5,
    "ai power shift": 2.2,
    "technological acceleration": 1.3,
    "economic expansion": 1.2,
    "social unrest": 1.4,
    "emerging pattern": 1.0
}

learning = LearningPipeline(weights=WEIGHTS)


# SAFE HELPERS
def safe_list(x):
    return x if isinstance(x, list) else []


def safe_log(msg):
    try:
        logger.info(msg)
    except Exception:
        print(msg)


# MAIN ORCHESTRATOR
class Orchestrator:

    def run(self):

        start_time = time.time()

        try:
            safe_log("ORCHESTRATOR START")

            # 1. CRAWL
            raw_data = safe_list(crawl())
            safe_log(f"[1] Crawled: {len(raw_data)}")

            if not raw_data:
                return []

            # 2. PROCESS
            processed = safe_list(process_data(raw_data))
            safe_log(f"[2] Processed: {len(processed)}")

            if not processed:
                return []

            # 3. SIGNAL DETECTION
            signals = safe_list(detect_signals(processed))
            safe_log(f"[3] Signals: {len(signals)}")

            if not signals:
                return []

            # 4. ENRICH
            enriched = safe_list(enrich_intelligence(signals))
            safe_log(f"[4] Enriched: {len(enriched)}")

            if not enriched:
                return []

            # 5. MEMORY BOOST
            enriched = memory.boost(enriched)

            # 6. LEARNING
            enriched = safe_list(learning.run(enriched))

            # 7. MEMORY LEARN
            memory.learn(enriched)

            # 8. DECISION FILTER
            final = []
            seen = set()

            for item in enriched:
                try:
                    topic = str(item.get("topic", ""))

                    if not topic:
                        continue

                    if topic in seen:
                        continue

                    if should_generate(item):
                        seen.add(topic)
                        final.append(item)

                except Exception:
                    continue

            safe_log(f"[8] Final: {len(final)}")

            elapsed = round(time.time() - start_time, 3)
            safe_log(f"DONE in {elapsed}s")

            return final

        except Exception as e:
            safe_log("ORCHESTRATOR ERROR")
            safe_log(str(e))
            safe_log(traceback.format_exc())
            return []
