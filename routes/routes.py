from flask import Blueprint, render_template, request, redirect, url_for, session
import bcrypt

from database.db_ops import get_db_connection
from func.misc import slugify
from database.db_ops import get_latest_posts
from func.setup import check_setup, setup_blog

routes_bp = Blueprint('routes', __name__)  # Create a Blueprint

@routes_bp.route('/')
def index():
    if check_setup() == 0:
        return redirect(url_for('routes.setup'))
    posts = get_latest_posts()
    return render_template('index.html', posts=posts)

@routes_bp.route('/setup', methods=['GET', 'POST'])
def setup():
    if check_setup() == 1:
        return redirect(url_for('routes.index'))  # Redirect if already set up

    if request.method == 'POST':
        blog_title = request.form.get('blog_title')  # Use .get() to avoid errors
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([blog_title, username, email, password]):
            return "Error: All fields are required!", 400  # Return 400 if missing fields

        setup_blog(blog_title, username, email, password)

        if check_setup() == 1:
            return redirect(url_for('routes.index'))
        else:
            return "Setup failed! Please contact support.", 500

    return render_template('setup.html')

###################################################
@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login and session management."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch user by email
        cursor.execute("SELECT email, username, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode("utf-8")):
            # Store user session
            session['email'] = user["email"]
            session['username'] = user["username"]
            return redirect(url_for('routes.index'))  # Redirect to dashboard after login

        return redirect(url_for('routes.index'))

    return render_template('login.html')

@routes_bp.route('/load-login-form', methods=['GET'])
def load_login_form():
    """Returns the login form as a partial for HTMX."""
    return render_template("partials/login_form.html")

######################################################

@routes_bp.route('/logout')
def logout():
    """Clears user session and reloads the auth container."""
    session.clear()
    return '<button hx-get="' + url_for('routes.load_login_form') + '" hx-target="#auth-container" hx-swap="outerHTML" class="login-btn">Login</button>'


@routes_bp.route('/create-post')
def create_post():
    """Allows users, if logged in, to create / add new posts"""
    if 'email' not in session:
        return redirect(url_for('routes.login'))  # Redirect to login if not logged in
    

@routes_bp.route('/admin')
def admin():
    """Allows users, if logged in, to manage their blog"""
    if 'email' not in session:
        return redirect(url_for('routes.login'))  # Redirect to login if not logged in