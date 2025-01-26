import bcrypt

def hash_password(password):
    """Hash a password for storing in the database."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    """Verify the entered password against stored hash."""
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

hashed_pw = hash_password("securepassword")
is_valid = check_password(hashed_pw, "securepassword")  # Returns True
