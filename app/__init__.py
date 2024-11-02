from flask import Flask
from .db import db  # Make sure to import the instance, not the module
from flask_login import LoginManager
from config import Config

# Initialize the login manager
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Redirect to the login page if not authenticated

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app instance
    db.init_app(app)  # Initialize the SQLAlchemy instance with the Flask app
    login_manager.init_app(app)  # Initialize Flask-Login with the app

    # Import and register blueprints (like routes)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Create database tables if they do not exist
    with app.app_context():
        db.create_all()  # This should call create_all on the SQLAlchemy instance

    return app

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login."""
    from .models import User  # Import User model inside the function to avoid circular imports
    return User.query.get(int(user_id))  # Fetch the user by their ID
