import re


def clean_text(text):

    if not text:
        return ""

    text = re.sub(r"<.*?>", "", text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def process_data(raw_data):

    processed = []

    for item in raw_data:

        title = clean_text(
            item.get("title", "")
        )

        # RSS fallback support
        content = clean_text(
            item.get("content", "") or
            item.get("summary", "") or
            item.get("description", "")
        )

        if not title or not content:
            continue

        processed.append({

            "title": title,
            "content": content,
            "text": f"{title} {content}",
            "source": item.get("source", "unknown")

        })

    print("pipeline processed:", len(processed))

    return processed
