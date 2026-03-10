import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

conn = None


def connect():

    global conn

    if conn is None:
        conn = psycopg2.connect(DATABASE_URL)

    return conn


def save_article(title, content):

    c = connect().cursor()

    c.execute(
        "INSERT INTO articles (title, content) VALUES (%s, %s)",
        (title, content)
    )

    connect().commit()

    c.close()
