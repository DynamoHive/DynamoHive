# backend/feed_engine.py

from backend.user_profile_engine import generate_feed, compute_final_score
from backend.events import detect_event_spikes


# -------------------------
# 🔥 SPIKE → BOOST MAP
# -------------------------

def build_spike_boost_map():
    spikes = detect_event_spikes()

    boost_map = {}

    for spike in spikes:
        topic = spike["topic"]

        # spike gücüne göre boost
        boost = spike["count"] * 0.5 + spike["velocity"] * 2

        boost_map[topic] = boost

    return boost_map


# -------------------------
# 🔥 FINAL SCORING (GLOBAL + USER + EVENT)
# -------------------------

def compute_total_score(signal, profile, boost_map):
    base_score = compute_final_score(signal, profile)

    topic = signal.get("topic")
    event_boost = boost_map.get(topic, 0)

    return base_score + event_boost


# -------------------------
# 🔥 MAIN FEED ENGINE
# -------------------------

def get_feed(user_id, signals):
    """
    signals = [
        {"topic": "ai", "score": 10},
        ...
    ]
    """

    # 1️⃣ user profile
    from backend.user_profile_engine import get_user_profile
    profile = get_user_profile(user_id)

    # 2️⃣ spike boost map
    boost_map = build_spike_boost_map()

    # 3️⃣ ranking
    ranked = sorted(
        signals,
        key=lambda s: compute_total_score(s, profile, boost_map),
        reverse=True
    )

    return ranked
