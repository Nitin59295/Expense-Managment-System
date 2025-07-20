from flask import Flask
from config import Config
from models import db
from routes import routes
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register the routes blueprint
app.register_blueprint(routes)

