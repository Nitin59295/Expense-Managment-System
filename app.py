"""
Main application entry point.
Initializes the Flask application, database, migration engine, and login manager.
"""
from flask import Flask
from config import Config
from models import db, User  # Import the new User model
from routes import routes
from flask_migrate import Migrate
from flask_login import LoginManager

# --- Application Factory ---
app = Flask(__name__)
app.config.from_object(Config)

# --- Initialize Extensions ---
db.init_app(app)
migrate = Migrate(app, db)

# --- Flask-Login Configuration ---
login_manager = LoginManager()
login_manager.init_app(app)
# Define the view to redirect to when a user needs to log in.
login_manager.login_view = 'routes.login'
login_manager.login_message_category = 'info' # Optional: for styling flash messages

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

# --- Register Blueprints ---
app.register_blueprint(routes)

