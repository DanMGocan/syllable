from flask import Flask
from func.setup import get_secret_key
from routes.routes import routes_bp  # Import Blueprint

app = Flask(__name__, template_folder='templates', static_folder="static")  

# Settings
app.config['SECRET_KEY'] = get_secret_key()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"  # Store session in files

# Register the blueprint
app.register_blueprint(routes_bp)

if __name__ == "__main__":
    app.run(debug=True)
