# backend/newsroom/article_engine.py

def generate_article(story):

    if not story:
        return None

    article = f"""
{story['title']}

Situation:
{story['summary']}

Signals:
{story['signals']}

Analysis:
{story['analysis']}

Implications:
{story['implications']}
"""

    return article
