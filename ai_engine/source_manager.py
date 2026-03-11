from ai_engine.source_manager import get_sources


def crawl():

    sources = get_sources()

    results = []

    for source in sources:

        if source["type"] == "rss":

            url = source["url"]

            # burada RSS çekme işlemi olacak
            # şimdilik örnek veri ekliyoruz

            results.append({
                "text": f"data from {url}"
            })

    return results
