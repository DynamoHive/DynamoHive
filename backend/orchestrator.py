def _generate_content(self, intelligence):

    logger.info(f"[CONTENT] incoming: {len(intelligence) if intelligence else 0}")

    if not intelligence:
        logger.info("[CONTENT] no intelligence")
        return

    for intel in intelligence:

        try:
            topic = str(intel.get("topic", "")).strip()
        except:
            continue

        if not topic:
            continue

        # -------------------------
        # NARRATIVE
        # -------------------------
        try:
            if generate_narrative:
                content = generate_narrative(intel)
            else:
                content = {"title": topic, "content": topic}
        except Exception as e:
            logger.warning(f"[NARRATIVE ERROR] {e}")
            content = {"title": topic, "content": topic}

        if not content:
            continue

        title = content.get("title")
        body = content.get("content")

        if not title or not body:
            continue

        # -------------------------
        # SAVE
        # -------------------------
        try:
            if save_post:
                save_post(title, body)
        except Exception as e:
            logger.warning(f"[SAVE ERROR] {e}")

        # -------------------------
        # DISTRIBUTE
        # -------------------------
        try:
            if distribute:
                distribute(content)
        except Exception as e:
            logger.warning(f"[DISTRIBUTION ERROR] {e}")

        logger.info(f"[GENERATED] {topic}")
