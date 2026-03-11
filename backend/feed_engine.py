feed_storage = []


def publish(items):

    if not items:
        return

    for item in items:
        feed_storage.append(item)


def get_feed():

    return {
        "items": feed_storage[-20:]
    }
