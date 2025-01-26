# Flask dependencies
from flask import render_template, request, redirect, url_for

# Universal database connector
from database.db_ops import get_db_connection

from app import app
from func.misc import slugify
from database.db_ops import get_latest_posts
from func.setup import check_setup, setup_blog, get_secret_key

# Main page
@app.route('/')
def index():
    if check_setup() == 0:
        return redirect(url_for('setup'))
    posts = get_latest_posts()
    return render_template('index.html', posts=posts)


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

        if check_setup() == 1:
            return redirect(url_for('index'))
        else:
            return "Setup failed! Unsure why. Please contact me at gocandan@gmail.com and we'll work it out :)", 500
    
    return render_template('setup.html')

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    return "Login Page (Under Construction)"
