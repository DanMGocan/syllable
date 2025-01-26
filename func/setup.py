from db_ops import get_db_connection
import secrets

def check_setup():
    """Check if the blog has already been set up."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT setup_flag FROM settings LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0  # Return 1 if setup exists, otherwise 0

def setup_blog(blog_title, username, email, password):
    """Initialize the blog by creating tables and storing setup details."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Generate a random secret key
    secret_key = secrets.token_hex(32)

    # Insert data into tables
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                   (username, email, password))
    
    cursor.execute("INSERT INTO settings (blog_title, secret_key, setup_flag) VALUES (?, ?, 1)", 
                   (blog_title, secret_key))
    
    conn.commit()
    conn.close()

def get_secret_key():
    """Retrieve the secret key from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT secret_key FROM settings LIMIT 1")
    secret_key = cursor.fetchone()
    conn.close()
    return secret_key[0] if secret_key else None
