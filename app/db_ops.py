import sqlite3
import bcrypt

DB_NAME = "blog.db"

def check_setup():
    """Check if the blog is initialized (returns 1 if setup, else 0)."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT is_setup FROM settings LIMIT 1")
    setup_status = c.fetchone()
    
    conn.close()
    return setup_status[0] if setup_status else 0  # Return 0 if no settings row exists

def setup_blog(blog_title, username, email, password):
    """Initialize blog settings and create admin user."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Ensure the settings table has at least one row
    c.execute("SELECT COUNT(*) FROM settings")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO settings (blog_name, is_setup) VALUES (?, 0)", (blog_title,))

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert admin user
    c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
              (username, email, hashed_password))

    # Update blog settings and mark setup as complete
    c.execute("UPDATE settings SET blog_name = ?, is_setup = 1 WHERE id = 1", (blog_title,))

    conn.commit()
    conn.close()

def get_latest_posts():
    """Fetch latest blog posts."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, content, views FROM posts ORDER BY date_posted DESC LIMIT 5")
    posts = c.fetchall()
    conn.close()
    return posts