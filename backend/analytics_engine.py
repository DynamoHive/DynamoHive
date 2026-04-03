from backend.events import detect_event_spikes


def get_topic_boost():
    spikes = detect_event_spikes()

    boost_map = {}

    for s in spikes:
        topic = str(s.get("topic", "")).lower()

        count = s.get("count", 0)
        velocity = s.get("velocity", 0)

        # 🔥 güvenli hesaplama
        try:
            boost = (count * 5) + (velocity * 10)
        except:
            boost = 0

        boost_map[topic] = boost

    return boost_map
