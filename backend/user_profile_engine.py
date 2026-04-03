# backend/user_profile_engine.py

user_profiles = {}

def get_user_profile(user_id):
    if user_id not in user_profiles:
        user_profiles[user_id] = {
            "interests": {},
            "affinity": {},
            "history": [],
            "engagement": 0
        }
    return user_profiles[user_id]


# -------------------------
# UPDATE FUNCTIONS
# -------------------------

def update_interest(profile, topic, value):
    profile["interests"][topic] = profile["interests"].get(topic, 0) + value


def update_affinity(profile, topic, value):
    profile["affinity"][topic] = profile["affinity"].get(topic, 0) + value


def update_engagement(profile, event):
    if event["type"] in ["click", "like"]:
        profile["engagement"] += 1


# -------------------------
# EVENT PROCESSING
# -------------------------

def process_event(user_id, event):
    profile = get_user_profile(user_id)

    profile["history"].append(event)

    topic = event.get("topic")

    if event["type"] == "click":
        update_interest(profile, topic, 2)     # 🔥 artırıldı

    elif event["type"] == "like":
        update_affinity(profile, topic, 3)     # 🔥 artırıldı

    elif event["type"] == "skip":
        update_affinity(profile, topic, -2)

    update_engagement(profile, event)

    return profile


# -------------------------
# 🔥 STRONG USER BOOST
# -------------------------

def get_user_boost(profile, topic):
    interest = profile["interests"].get(topic, 0)
    affinity = profile["affinity"].get(topic, 0)

    # 🔥 çok daha güçlü etki
    return interest * 3 + affinity * 6


# -------------------------
# FINAL SCORE
# -------------------------

def compute_final_score(signal, profile):
    base = signal.get("score", 0)
    user_boost = get_user_boost(profile, signal.get("topic"))

    return base + user_boost


# -------------------------
# FEED GENERATION
# -------------------------

def generate_feed(user_id, signals):
    profile = get_user_profile(user_id)

    ranked = sorted(
        signals,
        key=lambda s: compute_final_score(s, profile),
        reverse=True
    )

    return ranked
