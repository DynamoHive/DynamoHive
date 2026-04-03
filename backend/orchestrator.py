import time
import traceback

from backend.logger import logger

# ENGINE IMPORTS
from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
import ai_engine.signal_detector as signal_module
from ai_engine.signal_ranking_engine import rank_signals

from backend.events import register_event, detect_event_spikes
from backend.user_profile_engine import get_user_profile, compute_final_score

from ai_engine.global_intelligence_engine import GlobalIntelligenceEngine
from ai_engine.narrative_engine import generate_narrative

from backend.storage import save_post, get_posts
from backend.cache import is_duplicate, mark_generated
from backend.distribution_engine import distribute


intel_engine = GlobalIntelligenceEngine()


class Orchestrator:

    def __init__(self):
        self.cycle_count = 0
        self.last_run = None
        self.last_duration = 0
        self.last_signal_count = 0
        self.last_event_count = 0

    # -------------------------
    # 🔥 CORE FLOW
    # -------------------------

    def run_cycle(self):

        start = time.time()
        self.cycle_count += 1
        self.last_run = start

        logger.info(f"[ORCHESTRATOR] Cycle {self.cycle_count} started")

        try:

            # -------------------------
            # 1. DATA
            # -------------------------
            raw_data = crawl()

            if not raw_data:
                raw_data = get_posts() or [{"text": "bootstrap"}]

            raw_data = process_data(raw_data)

            # -------------------------
            # 2. SIGNAL
            # -------------------------
            signals = signal_module.detect_signals(raw_data)

            if not signals:
                signals = [{
                    "text": f"system_{int(time.time())}",
                    "score": 1
                }]

            signals = rank_signals(signals)

            self.last_signal_count = len(signals)

            # -------------------------
            # 3. EVENTS
            # -------------------------
            for s in signals:
                register_event(s.get("text"))

            events = detect_event_spikes()
            self.last_event_count = len(events)

            # -------------------------
            # 4. PERSONALIZATION
            # -------------------------
            profile = get_user_profile("global_user")

            for s in signals:
                topic = s.get("text")
                base_score = s.get("score", 0)

                s["score"] = compute_final_score(
                    {"topic": topic, "score": base_score},
                    profile
                )

            # -------------------------
            # 5. INTELLIGENCE
            # -------------------------
            intelligence = self._build_intelligence(signals, events)

            try:
                intelligence = intel_engine.process(intelligence)
            except Exception as e:
                logger.warning(f"[INTEL ERROR] {e}")

            # -------------------------
            # 6. CONTENT
            # -------------------------
            self._generate_content(intelligence)

        except Exception:
            traceback.print_exc()

        finally:
            duration = round(time.time() - start, 2)
            self.last_duration = duration

            logger.info(f"[ORCHESTRATOR] Cycle finished in {duration}s")

    # -------------------------
    # 🧠 INTELLIGENCE BUILDER
    # -------------------------

    def _build_intelligence(self, signals, events):

        intelligence = []

        for s in signals:
            topic = s.get("text") or "unknown"

            intelligence.append({
                "topic": topic,
                "summary": f"{topic} shows emerging structural signals in global systems.",
                "trend": "surging" if s.get("score", 0) > 3 else "rising"
            })

        return intelligence

    # -------------------------
    # 📰 CONTENT ENGINE
    # -------------------------

    def _generate_content(self, intelligence):

        for intel in intelligence:

            base_topic = intel.get("topic") or "unknown"

            if is_duplicate(base_topic):
                topic = f"{base_topic}_{int(time.time())}"
            else:
                topic = base_topic

            content = generate_narrative(intel)

            if not content:
                continue

            title = content.get("title") or topic
            body = content.get("content") or "No content"

            try:
                save_post(title, body)
            except Exception:
                logger.warning("[SAVE ERROR]")
                continue

            try:
                distribute(content)
            except Exception:
                logger.warning("[DISTRIBUTION ERROR]")

            try:
                mark_generated(topic)
            except Exception:
                logger.warning("[CACHE ERROR]")

            logger.info(f"[ORCHESTRATOR] GENERATED: {topic}")

    # -------------------------
    # 🔥 STATUS (KOD-9)
    # -------------------------

    def get_status(self):
        return {
            "cycle_count": self.cycle_count,
            "last_run": self.last_run,
            "last_duration": self.last_duration,
            "last_signal_count": self.last_signal_count,
            "last_event_count": self.last_event_count
        }
