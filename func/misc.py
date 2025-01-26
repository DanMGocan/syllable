import re
import sqlite3

# Database name 
DB_NAME = "blog.db"

def slugify(title):
    """Convert a blog post title into a URL-friendly slug."""
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title)  # Remove special chars
    slug = slug.lower().strip().replace(" ", "-")  # Replace spaces with "-"
    return slug

