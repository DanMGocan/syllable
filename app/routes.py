from flask import render_template, request, redirect, url_for
import sqlite3
from app import app
from app.utils import slugify
from app.db_ops import check_setup, setup_blog, get_latest_posts

# Main page
@app.route('/')
def index():
    if check_setup() == 0:
        return redirect(url_for('setup'))
    posts = get_latest_posts()
    return render_template('index.html', posts=posts)

# Route for setting up the blog on first run
@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if check_setup() == 1:
        return redirect(url_for('index'))  # Redirect if already set up

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        setup_blog(blog_title, username, email, password)

        # Double-check if the setup flag is updated
        if check_setup() == 1:
            return redirect(url_for('index'))
        else:
            return "Setup failed. Please try again.", 500
    
    return render_template('setup.html')

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    return "Login Page (Under Construction)"
