content = generate_content(event)

if not isinstance(content, dict):
    logger.warning("invalid content format, skipping")
    continue

title = content.get("title", f"Event: {event.get('topic')}")
body = content.get("content", "")

save_post(title, body)

distribute({
    "title": title,
    "content": body
})
