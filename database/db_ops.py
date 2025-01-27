import sqlite3
import bcrypt

DB_NAME = "database/blog.db"

def get_db_connection():
    """Universal database connector, to be used in all the modules"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def get_latest_posts():
    """Fetch latest blog posts."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, content, views FROM posts ORDER BY date_posted DESC LIMIT 5")
    posts = c.fetchall()
    conn.close()
    return posts