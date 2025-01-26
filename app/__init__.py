from flask import Flask

app = Flask(__name__, template_folder = '../templates')
app.config['SECRET_KEY'] = '1234567890'

from app import routes  # Import routes after app initialization
