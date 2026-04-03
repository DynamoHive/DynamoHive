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


def update_interest(profile, topic, value):
    profile["interests"][topic] = profile["interests"].get(topic, 0) + value


def update_affinity(profile, topic, value):
    profile["affinity"][topic] = profile["affinity"].get(topic, 0) + value


def update_engagement(profile, event):
    if event["type"] in ["click", "like"]:
        profile["engagement"] += 1


def process_event(user_id, event):
    profile = get_user_profile(user_id)

    profile["history"].append(event)

    if event["type"] == "click":
        update_interest(profile, event["topic"], 1)

    elif event["type"] == "like":
        update_affinity(profile, event["topic"], 2)

    elif event["type"] == "skip":
        update_affinity(profile, event["topic"], -1)

    update_engagement(profile, event)

    return profile


def get_user_boost(profile, topic):
    interest = profile["interests"].get(topic, 0)
    affinity = profile["affinity"].get(topic, 0)

    return interest * 0.5 + affinity * 1.5


def compute_final_score(signal, profile):
    base = signal.get("score", 0)
    user_boost = get_user_boost(profile, signal.get("topic"))

    return base + user_boost


def generate_feed(user_id, signals):
    profile = get_user_profile(user_id)

    ranked = sorted(
        signals,
        key=lambda s: compute_final_score(s, profile),
        reverse=True
    )

    return ranked
