import time
import traceback
import hashlib

from backend.logger import logger

# --- SAFE IMPORTS (hiçbiri sistemi düşürmesin)
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


# -------------------------
# GLOBALS
# -------------------------
GLOBAL_DATA = []
_duplicate_cache = {}


# -------------------------
# HELPERS
# -------------------------
def is_duplicate_local(topic: str) -> bool:
    try:
        key = hashlib.md5(topic.lower().strip().encode()).hexdigest()
    except:
        return False

    now = time.time()
    if key in _duplicate_cache and (now - _duplicate_cache[key] < 3600):
        return True

    _duplicate_cache[key] = now
    return False


def normalize_signals(signals):
    out = []
    for s in signals or []:
        topic = str(s.get("topic") or s.get("title") or s.get("text") or "").strip()
        if len(topic) < 5:
            continue
        out.append({
            "topic": topic,
            "score": float(s.get("score", 1.0))
        })
    return out


def force_signals(raw_data):
    forced = []
    for item in (raw_data or [])[:5]:
        text = (item.get("title") or item.get("text") or "").strip()
        if text:
            forced.append({"topic": text, "score": 1.0})
    return forced


def safe_generate_content(intel):
    # narrative engine varsa kullan, yoksa fallback
    try:
        if generate_narrative:
            c = generate_narrative(intel)
            if isinstance(c, dict) and c.get("title") and c.get("content"):
                return c
    except:
        pass

    topic = str(intel.get("topic", ""))[:120]
    return {"title": topic, "content": topic}


# -------------------------
# ORCHESTRATOR
# -------------------------
class Orchestrator:

    def __init__(self):
        self.cycle = 0
        self.pattern_memory = MemoryPatternEngine()

    def run_cycle(self):
        t0 = time.time()
        self.cycle += 1
        logger.info(f"[ORCHESTRATOR] Cycle {self.cycle} started")

        try:
            # ---- DATA
            raw = crawl() or []
            if not raw:
                raw = [{"text": "bootstrap signal"}]

            raw = process_data(raw) or raw

            GLOBAL_DATA.clear()
            GLOBAL_DATA.extend(raw[:100])

            # ---- SIGNALS
            signals = detect_signals(raw) or []
            signals = normalize_signals(signals)

            # 🔥 CRITICAL: boşsa zorla üret
            if not signals:
                logger.info("[FORCE SIGNAL]")
                signals = force_signals(raw)

            # ---- EVENTS (opsiyonel)
            for s in signals:
                try:
                    register_event(s["topic"])
                except:
                    pass
            try:
                _ = detect_event_spikes()
            except:
                pass

            # ---- PERSONALIZE (opsiyonel)
            profile = get_user_profile("global_user")
            for s in signals:
                try:
                    s["score"] = compute_final_score(s, profile)
                except:
                    pass

            # ---- CONTENT
            self._generate(signals)

        except Exception:
            traceback.print_exc()

        finally:
            dt = round(time.time() - t0, 2)
            logger.info(f"[ORCHESTRATOR] Cycle finished in {dt}s")

    # -------------------------
    def _generate(self, items):
        generated = 0

        for intel in items:
            topic = str(intel.get("topic", "")).strip()
            if len(topic) < 5:
                continue

            if is_duplicate_local(topic):
                continue

            if self.pattern_memory.seen_before(topic):
                continue

            # similarity gate (yumuşak)
            try:
                sims = search_similar(topic) or []
                if sims and sims[0].get("score", 0) > 0.95:
                    continue
            except:
                pass

            content = safe_generate_content(intel)
            title = content.get("title")
            body = content.get("content")

            if not title or not body:
                continue

            if is_low_quality(body):
                continue

            if len(body) < 40:
                # çok kısa ise yine de kaydet (minimum akış için)
                body = body + "."

            try:
                save_post(title, body)
            except:
                pass

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
            # 🔥 son çare: tek zorunlu içerik
            fallback = items[0] if items else {"topic": "fallback signal"}
            topic = str(fallback.get("topic", "fallback signal"))[:120]
            content = {"title": topic, "content": topic}
            try:
                save_post(content["title"], content["content"])
            except:
                pass
            logger.info("[ORCHESTRATOR] GENERATED (FORCED): fallback")
