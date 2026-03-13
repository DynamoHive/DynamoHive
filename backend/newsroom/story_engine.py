def build_story(intelligence):

    if not intelligence:
        return None

    story = {
        "title": intelligence.get("title", "DynamoHive Intelligence"),
        "summary": intelligence.get("summary"),
        "signals": intelligence.get("signals", []),
        "analysis": intelligence.get("analysis"),
        "implications": intelligence.get("implications")
    }

    return story
