import re

from backend.logger import logger


# =====================================================
# CLEAN
# =====================================================

def clean_text(text):

    if not text:
        return ""

    text = str(text)

    text = re.sub(r"<.*?>", "", text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =====================================================
# PROCESS
# =====================================================

def process_data(raw_data):

    processed = []

    for item in raw_data:

        title = clean_text(item.get("title"))

        # SAFE FALLBACKS
        content = clean_text(
            item.get("content")
            or item.get("summary")
            or item.get("description")
            or item.get("text")
            or ""
        )

        # title yoksa skip
        if not title:
            continue

        # content boşsa title kullan
        if not content:
            content = title

        processed.append({
            "title": title,
            "content": content,
            "text": f"{title} {content}",
            "source": item.get("source", "unknown"),
            "link": item.get("link", "")
        })

    logger.info(f"[DATA PIPELINE] processed: {len(processed)}")

    return processed
