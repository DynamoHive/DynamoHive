📁 backend/orchestrator.py (FINAL)
import time
import traceback

from backend.logger import logger

# -------------------------
# ENGINE IMPORTS
# -------------------------
from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.signal_detector import detect_signals

from ai_engine.intelligence.enrich_intelligence import enrich_intelligence
from ai_engine.intelligence.decision_engine import should_generate

from ai_engine.intelligence.memory_engine import MemoryEngine
from ai_engine.intelligence.learning_pipeline import LearningPipeline

# -------------------------
# INIT SYSTEMS
# -------------------------
memory = MemoryEngine()
learning = LearningPipeline(weights={
    "geopolitical escalation": 2.5,
    "system instability": 1.5,
    "ai power shift": 2.2,
    "technological acceleration": 1.3,
    "economic expansion": 1.2,
    "social unrest": 1.4,
    "emerging pattern": 1.0
})

# -------------------------
# SAFE HELPERS
# -------------------------
def safe_list(x):
    return x if isinstance(x, list) else []

def safe_log(msg):
    try:
        logger.info(msg)
    except:
        print(msg)

# -------------------------
# MAIN ORCHESTRATOR
# -------------------------
class Orchestrator:

    def run(self):

        start_time = time.time()

        try:
            safe_log("🚀 ORCHESTRATOR START")

            # -------------------------
            # 1. CRAWL
            # -------------------------
            raw_data = crawl()
            raw_data = safe_list(raw_data)
            safe_log(f"[1] Crawled: {len(raw_data)} items")

            if not raw_data:
                return []

            # -------------------------
            # 2. PROCESS
            # -------------------------
            processed = process_data(raw_data)
            processed = safe_list(processed)
            safe_log(f"[2] Processed: {len(processed)} items")

            if not processed:
                return []

            # -------------------------
            # 3. SIGNAL DETECTION
            # -------------------------
            signals = detect_signals(processed)
            signals = safe_list(signals)
            safe_log(f"[3] Signals: {len(signals)}")

            if not signals:
                return []

            # -------------------------
            # 4. INTELLIGENCE ENRICH
            # -------------------------
            enriched = enrich_intelligence(signals)
            enriched = safe_list(enriched)
            safe_log(f"[4] Enriched: {len(enriched)}")

            if not enriched:
                return []

            # -------------------------
            # 5. MEMORY BOOST
            # -------------------------
            enriched = memory.boost(enriched)
            safe_log("[5] Memory boost applied")

            # -------------------------
            # 6. LEARNING (KOD 7)
            # -------------------------
            enriched = learning.run(enriched)
            enriched = safe_list(enriched)
            safe_log("[6] Learning pipeline applied")

            # -------------------------
            # 7. MEMORY LEARN
            # -------------------------
            memory.learn(enriched)
            safe_log("[7] Memory updated")

            # -------------------------
            # 8. DECISION FILTER
            # -------------------------
            final = []

            for item in enriched:
                try:
                    if should_generate(item):
                        final.append(item)
                except:
                    continue

            safe_log(f"[8] Final Output: {len(final)}")

            # -------------------------
            # DONE
            # -------------------------
            elapsed = round(time.time() - start_time, 3)
            safe_log(f"✅ DONE in {elapsed}s")

            return final

        except Exception as e:

            safe_log("❌ ORCHESTRATOR ERROR")
            safe_log(str(e))
            safe_log(traceback.format_exc())

            return []
