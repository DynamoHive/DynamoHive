import time
import traceback
import hashlib
from ai_engine.intelligence_layer import enrich_intelligence
from ai_engine.power_mapping_engine import map_power
from backend.logger import logger

# SAFE IMPORTS
try:
    from ai_engine.multi_crawler import crawl
except:
    def crawl(): return []

try:
    from ai_engine.data_pipeline import process_data
except:
    def process_data(x): return x

try:
    import ai_engine.signal_detector as signal_module
    detect_signals = getattr(signal_module, "detect_signals", lambda x: [])
except:
    def detect_signals(x): return []

try:
    from backend.events import register_event, detect_event_spikes
except:
    def register_event(*a, **k): pass
    def detect_event_spikes(): return []

try:
    from backend.user_profile_engine import get_user_profile, compute_final_score
except:
    def get_user_profile(*a, **k): return {}
    def compute_final_score(s, p): return s.get("score", 1.0)

try:
    from backend.storage import save_post
except:
    def save_post(*a, **k): pass

try:
    from backend.distribution_engine import distribute
except:
    def distribute(*a, **k): pass

try:
    from ai_engine.memory_pattern_engine import MemoryPatternEngine
except:
    class MemoryPatternEngine:
        def seen_before(self, *a, **k): return False
        def store(self, *a, **k): pass

try:
    from ai_engine.content_filter import is_low_quality
except:
    def is_low_quality(x): return False

try:
    from ai_engine.vector_memory import search_similar, store_vector
except:
    def search_similar(*a, **k): return []
    def store_vector(*a, **k): pass

try:
    from ai_engine.narrative_engine import generate_narrative
except:
    generate_narrative = None


# GLOBALS
GLOBAL_DATA = []
duplicate_cache = {}


def is_duplicate_local(topic):
    try:
        h = hashlib.md5(topic.lower().encode()).hexdigest()
    except:
        return False

    now = time.time()

    if h in duplicate_cache and now - duplicate_cache[h] < 3600:
        return True

    duplicate_cache[h] = now
    return False


def force_signals(raw_data):
    out = []
    for item in raw_data[:5]:
        text = item.get("title") or item.get("text") or ""
        if text:
            out.append({"topic": text, "score": 1.0})
    return out


def safe_generate(intel):
    try:
        if generate_narrative:
            c = generate_narrative(intel)
            if c and c.get("title") and c.get("content"):
                return c
    except:
        pass

    topic = str(intel.get("topic", ""))
    return {
        "title": topic[:80],
        "content": topic
    }


class Orchestrator:

    def __init__(self):
        self.cycle = 0
        self.pattern_memory = MemoryPatternEngine()

    def run_cycle(self):

        start = time.time()
        self.cycle += 1

        logger.info(f"[ORCHESTRATOR] Cycle {self.cycle} started")

        try:
            # DATA
            raw = crawl() or [{"text": "fallback"}]
            raw = process_data(raw)

            GLOBAL_DATA.clear()
            GLOBAL_DATA.extend(raw[:100])

            # SIGNAL
            signals = detect_signals(raw)

            if not signals:
                logger.info("[FORCE SIGNAL]")
                signals = force_signals(raw)

            # PERSONALIZE
            profile = get_user_profile("global_user")

            for s in signals:
                try:
                    s["score"] = compute_final_score(s, profile)
                except:
                    pass

            # CONTENT
            self._generate(signals)

        except Exception:
            traceback.print_exc()

        finally:
            duration = round(time.time() - start, 2)
            logger.info(f"[ORCHESTRATOR] Cycle finished in {duration}s")

    def _generate(self, items):

        MAX_POSTS = 5
        generated = 0

        for intel in items:

            if generated >= MAX_POSTS:
                break

            topic = str(intel.get("topic", "")).strip()

            if len(topic) < 5:
                continue

            if is_duplicate_local(topic):
                continue

            if self.pattern_memory.seen_before(topic):
                continue

            try:
                sims = search_similar(topic)
                if sims and sims[0].get("score", 0) > 0.95:
                    continue
            except:
                pass

            content = safe_generate(intel)

            title = content.get("title")
            body = content.get("content")

            if not title or not body:
                continue

            if is_low_quality(body):
                continue

            if len(body) < 40:
                body += "."

            try:
                save_post(title, body)
            except:
                continue

            try:
                store_vector(content)
            except:
                pass

            try:
                distribute(content)
            except:
                pass

            self.pattern_memory.store(topic)
            generated += 1

            logger.info(f"[ORCHESTRATOR] GENERATED: {topic}")

        if generated == 0:
            topic = "fallback signal"
            try:
                save_post(topic, topic)
            except:
                pass
            logger.info("[ORCHESTRATOR] GENERATED (FORCED)")
