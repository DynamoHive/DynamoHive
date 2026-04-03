def is_low_quality(text):

    if not text:
        return True

    text = text.strip()

    if len(text) < 120:
        return True

    words = text.lower().split()

    if not words:
        return True

    unique_ratio = len(set(words)) / len(words)

    if unique_ratio < 0.4:
        return True

    return False
