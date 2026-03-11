import psycopg2
import os
from pathlib import Path

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()


def init_database():

    schema_path = Path(__file__).resolve().parent / "schema.sql"

    with open(schema_path, "r") as f:

        cursor.execute(f.read())

    conn.commit()
