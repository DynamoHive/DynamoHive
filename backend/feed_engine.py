from database import save_post


def publish(post):

    title = post.get("title", "analysis")

    content = post.get("content", "")

    save_post(title, content)
