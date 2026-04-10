import time
import traceback
import hashlib

from backend.logger import logger

from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.signal_detector import detect_signals
from ai_engine.signal_ranking_engine import merge_ranked_signals

from ai_engine.global_intelligence_engine import GlobalIntelligenceEngine
from ai_engine.decision_engine import DecisionEngine

from backend.storage import save_post


LAST_DATA = []
duplicate_cache = {}


def is_duplicate(topic):
    try:
        h = hashlib.md5(str(topic).lower().encode()).hexdigest()
    except:
        return False

    now = time.time()

    if h in duplicate_cache and now - duplicate_cache[h] < 3600:
        return True

    duplicate_cache[h] = now
    return False


class Orchestrator:

    def __init__(self):
        self.cycle = 0
        self.intelligence = GlobalIntelligenceEngine()
        self.decision = DecisionEngine()

    def run_cycle(self):

        start = time.time()
        self.cycle += 1

        logger.info(f"[ORCHESTRATOR] Cycle {self.cycle} started")

        try:
            # -------------------------
            # 1. DATA
            # -------------------------
            raw = crawl()

            if not raw:
                raw = LAST_DATA or [{"title": "fallback signal"}]

            raw = process_data(raw)

            LAST_DATA.clear()
            LAST_DATA.extend(raw[:100])

            # -------------------------
            # 2. SIGNALS
            # -------------------------
            signals = detect_signals(raw)

            if not signals:
                signals = [
                    {"topic": str(x.get("title") or "fallback"), "score": 1.0}
                    for x in raw[:5]
                ]

            # -------------------------
            # 3. RANK
            # -------------------------
            signals = merge_ranked_signals(signals)

            # -------------------------
            # 4. INTELLIGENCE
            # -------------------------
            intel_items = self.intelligence.run(signals)

            print("INTEL COUNT:", len(intel_items))

            if not intel_items:
                logger.warning("[ORCHESTRATOR] No intelligence output")
                return

            # -------------------------
            # 5. DECISION
            # -------------------------
            decisions = self.decision.evaluate(intel_items)

            print("DECISIONS:", decisions)

            # 🔥 FORCE MODE (KRİTİK)
            decisions = decisions or intel_items

            # -------------------------
            # 6. GENERATION
            # -------------------------
            generated = 0

            for item in decisions:

                try:
                    topic = str(item.get("topic") or "").strip()

                    if not topic:
                        continue

                    if is_duplicate(topic):
                        continue

                    # 🔥 FORCE PUBLISH (TEST MODE)
                    publish = True

                    if not publish:
                        print("SKIPPED:", topic)
                        continue

                    narrative = item.get("narrative") or {}

                    title = narrative.get("title") or topic[:80]
                    content = narrative.get("content") or topic

                    print("GENERATING:", title)

                    save_post(title, content)

                    generated += 1

                    logger.info(
                        f"[GENERATED] {topic} | priority={item.get('decision', {}).get('priority', 'N/A')}"
                    )

                except Exception as e:
                    print("GEN ERROR:", e)
                    continue

            print("GENERATED COUNT:", generated)

            if generated == 0:
                logger.warning("[ORCHESTRATOR] NOTHING GENERATED")

        except Exception:
            traceback.print_exc()

        finally:
            duration = round(time.time() - start, 2)
            logger.info(f"[ORCHESTRATOR] Cycle finished in {duration}s")
