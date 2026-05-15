import time
import traceback
import hashlib

from backend.logger import logger
from backend.storage import save_signal

from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
from ai_engine.signal_detector import detect_signals
from ai_engine.signal_ranking_engine import merge_ranked_signals
from ai_engine.signal_cluster import cluster_signals

from ai_engine.global_intelligence_engine import GlobalIntelligenceEngine
from ai_engine.decision_engine import DecisionEngine
from ai_engine.global_crisis_radar import detect_crisis_signals


# =====================================================
# MEMORY
# =====================================================

LAST_DATA = []
duplicate_cache = {}

DEBUG_MODE = True
FORCE_OUTPUT = False


def is_duplicate(topic: str) -> bool:
    try:
        time_bucket = int(time.time() / 300)
        key = hashlib.md5(
            (str(topic).lower() + str(time_bucket)).encode()
        ).hexdigest()
    except Exception:
        return False

    now = time.time()

    if key in duplicate_cache:
        if now - duplicate_cache[key] < 300:
            if DEBUG_MODE:
                logger.info(f"[DUPLICATE BLOCKED] {topic}")
            return True

    duplicate_cache[key] = now

    if len(duplicate_cache) > 10000:
        duplicate_cache.clear()

    return False


# =====================================================
# ORCHESTRATOR
# =====================================================

class Orchestrator:

    def __init__(self):
        self.cycle = 0
        self.intelligence = GlobalIntelligenceEngine()
        self.decision = DecisionEngine()

    def run_cycle(self):

        start = time.time()
        self.cycle += 1

        logger.info(f"\n==============================")
        logger.info(f"[ORCHESTRATOR] Cycle {self.cycle} START")
        logger.info(f"==============================")

        try:

            # =================================================
            # 1. CRAWL
            # =================================================
            raw = crawl()

            logger.info(f"[DEBUG] RAW CRAWL COUNT: {len(raw) if raw else 0}")

            if not raw:
                raw = LAST_DATA or [{
                    "title": "fallback signal",
                    "content": "fallback"
                }]

            logger.info(f"[DEBUG] RAW SAMPLE: {raw[:1]}")

            # =================================================
            # 2. PROCESS
            # =================================================
            raw = process_data(raw)

            logger.info(f"[DEBUG] AFTER PROCESS: {len(raw) if raw else 0}")

            if not raw:
                logger.warning("[PIPELINE STOP] process_data returned empty")
                return []

            LAST_DATA.clear()
            LAST_DATA.extend(raw[:100])

            # =================================================
            # 3. CRISIS DETECTION
            # =================================================
            crisis_signals = detect_crisis_signals(raw)

            logger.info(f"[DEBUG] CRISIS SIGNALS: {len(crisis_signals)}")

            crisis_map = {
                str(c.get("title", "")).lower(): c
                for c in crisis_signals
            }

            # =================================================
            # 4. SIGNAL DETECTION
            # =================================================
            signals = detect_signals(raw)

            logger.info(f"[DEBUG] SIGNALS FOUND: {len(signals) if signals else 0}")

            if not signals:
                signals = [{
                    "topic": x.get("title", "fallback"),
                    "score": 0.5
                } for x in raw[:10]]

            # =================================================
            # 5. RANK + CLUSTER
            # =================================================
            signals = merge_ranked_signals(signals or [])
            signals = cluster_signals(signals or [])

            logger.info(f"[DEBUG] AFTER CLUSTER: {len(signals)}")

            if not signals:
                logger.warning("[PIPELINE STOP] no signals after clustering")
                return []

            # =================================================
            # 6. CRISIS BOOST
            # =================================================
            for s in signals:

                topic = str(s.get("topic", "")).lower()

                if topic in crisis_map:
                    c = crisis_map[topic]
                    s["urgency"] = c.get("urgency", "high")
                    s["score"] = min(float(s.get("score", 0.5)) + 0.3, 1.0)

            # =================================================
            # 7. DECISION ENGINE
            # =================================================
            decisions = self.decision.evaluate(signals)

            logger.info(f"[DEBUG] DECISIONS: {len(decisions) if decisions else 0}")

            if not decisions:
                logger.warning("[PIPELINE STOP] no decisions")
                return []

            # =================================================
            # 8. INTELLIGENCE
            # =================================================
            intel = self.intelligence.run(decisions)

            logger.info(f"[DEBUG] INTELLIGENCE OUTPUT: {len(intel) if intel else 0}")

            if not intel:
                logger.warning("[PIPELINE STOP] no intelligence output")
                return []

            # merge decisions
            for i, item in enumerate(intel):
                if i < len(decisions):
                    item["decision"] = decisions[i]

            # =================================================
            # 9. GENERATION
            # =================================================
            output = []

            for item in intel:

                topic = str(item.get("topic", "")).strip()

                if not topic:
                    continue

                decision = item.get("decision", {})

                if not decision.get("publish", True):
                    if DEBUG_MODE:
                        logger.info(f"[SKIP PUBLISH] {topic}")
                    continue

                if is_duplicate(topic):
                    continue

                narrative = item.get("narrative") or {}

                title = narrative.get("title") or topic[:80]
                content = narrative.get("content") or topic

                payload = {
                    "title": title,
                    "topic": topic,
                    "content": content,
                    "priority": decision.get("priority", 0.5),
                    "published": True,
                    "timestamp": int(time.time())
                }

                save_signal(payload)

                output.append(payload)

                logger.info(f"[GENERATED] {topic} | priority={payload['priority']}")

            # =================================================
            # FINAL OUTPUT
            # =================================================
            logger.info(f"[DEBUG] FINAL OUTPUT COUNT: {len(output)}")

            if FORCE_OUTPUT and not output:
                logger.warning("[FORCE OUTPUT ENABLED] injecting fallback signal")

                output = [{
                    "title": "FORCED DEBUG SIGNAL",
                    "topic": "debug",
                    "content": "forced pipeline output",
                    "priority": 1.0,
                    "published": True,
                    "timestamp": int(time.time())
                }]

            return output

        except Exception as e:
            traceback.print_exc()
            logger.error(f"[ORCHESTRATOR ERROR] {str(e)}")
            return []

        finally:
            logger.info(
                f"[ORCHESTRATOR] Cycle finished in {round(time.time() - start, 2)}s"
            )
