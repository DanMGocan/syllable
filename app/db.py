import sqlite3
import bcrypt

DB_NAME = "blog.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    with open("schema.sql", "r") as f:
        c.executescript(f.read())  # Execute schema.sql to create tables

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")

