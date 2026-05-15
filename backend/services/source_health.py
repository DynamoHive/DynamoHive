import time

SOURCE_SCORE = {}
DECAY = 3600  # 1 hour


def update_source(url, success=True):
    now = time.time()

    if url not in SOURCE_SCORE:
        SOURCE_SCORE[url] = {"score": 1.0, "last": now}

    entry = SOURCE_SCORE[url]

    # decay over time
    if now - entry["last"] > DECAY:
        entry["score"] *= 0.9

    # update
    if success:
        entry["score"] = min(entry["score"] + 0.05, 1.5)
    else:
        entry["score"] *= 0.7

    entry["last"] = now


def get_source_weight(url):
    return SOURCE_SCORE.get(url, {}).get("score", 1.0)
