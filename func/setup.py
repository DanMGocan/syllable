from database.db_ops import get_db_connection
import secrets
import sqlite3
import bcrypt  # For password hashing

def check_setup():
    """Check if the blog has already been set up."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM settings")
    row_count = cursor.fetchone()[0]
    
    if row_count == 0:
        conn.close()
        return 0  # No setup found

    cursor.execute("SELECT setup_flag FROM settings LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else 0  # Return setup_flag if found, otherwise 0


def setup_blog(blog_title, username, email, password):
    """Initialize the blog by storing setup details while keeping the secret key intact."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Hash the password before storing
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Ensure only one row exists in settings
    cursor.execute("SELECT COUNT(*) FROM settings")
    row_count = cursor.fetchone()[0]

    if row_count == 0:
        # Insert a new settings row (first-time setup)
        cursor.execute("INSERT INTO settings (blog_title, secret_key, setup_flag) VALUES (?, ?, ?)", 
                       (blog_title, secrets.token_hex(32), 1))
    else:
        # Only update blog title and setup flag, keeping secret key the same
        cursor.execute("UPDATE settings SET blog_title = ?, setup_flag = 1 WHERE id = 1", 
                       (blog_title,))

    # Insert the admin user if users table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    if user_count == 0:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                       (username, email, hashed_password))

    conn.commit()
    conn.close()


def get_secret_key():
    """Retrieve the secret key from the database, or generate and store one if missing."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the settings table has data
    cursor.execute("SELECT id, secret_key FROM settings LIMIT 1")
    result = cursor.fetchone()

    if result:
        secret_key = result[1]  # Use existing secret key
    else:
        # Generate and insert a new secret key if settings table is empty
        secret_key = secrets.token_hex(32)
        cursor.execute("INSERT INTO settings (blog_title, secret_key, setup_flag) VALUES (?, ?, ?)", 
                       ("Default Blog", secret_key, 0))

    conn.commit()
    conn.close()
    return secret_key
