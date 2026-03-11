def analytics_engine(articles):

    if not articles:
        return {}

    stats = {
        "articles": len(articles)
    }

    print("Analytics:", stats)

    return stats
