import re
import sqlite3

# Database name 
DB_NAME = "blog.db"

def slugify(title):
    """Convert a blog post title into a URL-friendly slug."""
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title)  # Remove special chars
    slug = slug.lower().strip().replace(" ", "-")  # Replace spaces with "-"
    return slug

def check_setup():
    """Check if the blog is initialized, else prompt first-time setup."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT is_setup FROM settings LIMIT 1")
    setup_status = c.fetchone()
    conn.close()
    return setup_status[0] if setup_status else 0
