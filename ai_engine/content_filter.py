def is_low_quality(text):

    if not text:
        return True

    text = text.strip()

    if len(text) < 120:
        return True

    # çok tekrar eden kelime kontrolü
    words = text.lower().split()

    if len(words) == 0:
        return True

    unique_ratio = len(set(words)) / len(words)

    if unique_ratio < 0.4:
        return True

    return False
