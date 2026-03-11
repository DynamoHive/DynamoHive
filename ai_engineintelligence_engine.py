def intelligence_engine(articles):

    analysis = []

    for a in articles:

        text = f"""
Analysis: {a['title']}

The current development in technology indicates a broader
trend shaping global innovation ecosystems. Companies and
governments are increasingly competing for dominance in
critical technologies such as artificial intelligence,
semiconductors, and digital infrastructure.

Source: {a['link']}
"""

        analysis.append({
            "title": a["title"],
            "content": text
        })

    return analysis
