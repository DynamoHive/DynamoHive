import time
import traceback
import hashlib

from backend.logger import logger

from ai_engine.multi_crawler import crawl
from ai_engine.data_pipeline import process_data
import ai_engine.signal_detector as signal_module

from backend.events import register_event, detect_event_spikes
from backend.user_profile_engine import get_user_profile, compute_final_score

from backend.storage import save_post
from backend.distribution_engine import distribute

from ai_engine.memory_pattern_engine import MemoryPatternEngine
from ai_engine.content_filter import is_low_quality
from ai_engine.vector_memory import search_similar, store_vector

# SAFE IMPORTS
try:
    from ai_engine.narrative_engine import generate_narrative
except:
    generate_narrative = None


# -------------------------
# GLOBAL
# -------------------------
GLOBAL_DATA = []
duplicate_cache = {}


# -------------------------
# DUPLICATE
# -------------------------
def is_duplicate_local(topic):
    try:
        topic = str(topic).lower().strip()
        h = hashlib.md5(topic.encode()).hexdigest()
    except:
        return False

    now = time.time()

    if h in duplicate_cache:
        if now - duplicate_cache[h] < 7200:
            return True

    duplicate_cache[h] = now
    return False


# -------------------------
# MERGE
# -------------------------
def merge_signals(signals):
    merged = {}

    for s in signals:
        topic = s["topic"]

        if topic not in merged:
            merged[topic] = s
        else:
            merged[topic]["score"] += s["score"]

    return list(merged.values())


# -------------------------
# ORCHESTRATOR
# -------------------------
class Orchestrator:

    def __init__(self):
        self.cycle_count = 0
        self.pattern_memory = MemoryPatternEngine()

    # -------------------------
    def run_cycle(self):

        start = time.time()
        self.cycle_count += 1

        logger.info(f"[ORCHESTRATOR] Cycle {self.cycle_count} started")

        try:
            # -------------------------
            # DATA
            # -------------------------
            raw_data = crawl()

            if not raw_data:
                raw_data = [{"text": "fallback signal"}]

            raw_data = process_data(raw_data)

            GLOBAL_DATA.clear()
            GLOBAL_DATA.extend(raw_data[:100])

            # -------------------------
            # SIGNAL
            # -------------------------
            signals = signal_module.detect_signals(raw_data)

            # 🔥 FORCE SIGNAL (CRITICAL FIX)
            if not signals:
                logger.info("[FORCE SIGNAL ACTIVATED]")

                for item in raw_data[:5]:
                    text = item.get("title") or item.get("text") or ""
                    if text:
                        signals.append({
                            "topic": text,
                            "score": 1.0
                        })

            signals = merge_signals(signals)

            # -------------------------
            # EVENTS
            # -------------------------
            for s in signals:
                register_event(s["topic"])

            events = detect_event_spikes()

            # -------------------------
            # PERSONALIZATION
            # -------------------------
            profile = get_user_profile("global_user")

            for s in signals:
                try:
                    s["score"] = compute_final_score(s, profile)
                except:
                    pass

            # -------------------------
            # CONTENT
            # -------------------------
            self._generate_content(signals)

        except Exception:
            traceback.print_exc()

        finally:
            duration = round(time.time() - start, 2)
            logger.info(f"[ORCHESTRATOR] Cycle finished in {duration}s")

    # -------------------------
    def _generate_content(self, intelligence):

        for intel in intelligence:

            topic = str(intel.get("topic", "")).strip()

            if not topic or len(topic) < 5:
                continue

            if is_duplicate_local(topic):
                continue

            if self.pattern_memory.seen_before(topic):
                continue

            similar = search_similar(topic)
            if similar:
                try:
                    if similar[0]["score"] > 0.92:
                        continue
                except:
                    pass

            # 🔥 SAFE NARRATIVE
            try:
                if generate_narrative:
                    content = generate_narrative(intel)
                else:
                    raise Exception("no narrative engine")
            except:
                content = {
                    "title": topic[:80],
                    "content": topic
                }

            title = content.get("title")
            body = content.get("content")

            if not title or not body:
                continue

            if is_low_quality(body):
                continue

            if len(body) < 50:
                continue

            try:
                save_post(title, body)
            except:
                continue

            self.pattern_memory.store(topic)

            try:
                store_vector(content)
            except:
                pass

            try:
                distribute(content)
            except:
                pass

            logger.info(f"[ORCHESTRATOR] GENERATED: {topic}")
