from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

POST_FILE = "storage/generated_posts.json"


def load_posts():

    if not os.path.exists(POST_FILE):
        return []

    posts = []

    with open(POST_FILE, "r") as f:
        for line in f:
            try:
                posts.append(json.loads(line))
            except:
                pass

    return posts


@app.route("/posts")
def get_posts():

    posts = load_posts()

    return jsonify(posts)


@app.route("/")
def home():

    return {"status": "DynamoHive API running"}


if __name__ == "__main__":
    app.run(port=5000)
