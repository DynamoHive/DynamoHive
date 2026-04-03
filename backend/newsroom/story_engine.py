def build_story(intelligence):

    if not intelligence:
        return None

    signals = intelligence.get("signals", [])

    if not signals:
        return None

    # -------------------------
    # 🔥 MAIN SIGNAL
    # -------------------------
    main = signals[0]

    topic = main.get("topic", "")
    keywords = main.get("keywords", [])
    count = main.get("count", 1)

    # -------------------------
    # 🔥 TITLE GENERATION
    # -------------------------
    title = topic.title()

    if count >= 5:
        title = f"Major Shift: {title}"
    elif count >= 3:
        title = f"Rising Signal: {title}"

    # -------------------------
    # 🔥 SUMMARY
    # -------------------------
    summary = f"{count} independent signals detected around '{topic}'."

    # -------------------------
    # 🔥 ANALYSIS
    # -------------------------
    if count >= 5:
        analysis = "This topic is rapidly gaining global traction and may indicate a major developing trend."
    elif count >= 3:
        analysis = "This signal is emerging across multiple sources and may evolve into a significant narrative."
    else:
        analysis = "This is an early signal detected within the data stream."

    # -------------------------
    # 🔥 IMPLICATIONS
    # -------------------------
    if any(k in keywords for k in ["war","conflict","attack"]):
        implications = "Potential geopolitical escalation or instability."
    elif any(k in keywords for k in ["ai","openai","technology","robot"]):
        implications = "Technological acceleration and competitive pressure likely."
    elif any(k in keywords for k in ["market","ipo","stock"]):
        implications = "Possible financial market impact or investment movement."
    else:
        implications = "Monitoring recommended as signal develops."

    # -------------------------
    # 🔥 FINAL STORY
    # -------------------------
    story = {
        "title": title,
        "summary": summary,
        "signals": signals[:5],
        "analysis": analysis,
        "implications": implications
    }

    return story
