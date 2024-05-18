from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "login"

def create_app(config_class='app.config.ProductionConfig'):

    app = Flask(__name__)
    CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for the application.
    
    app.config.from_object(config_class)  # Load configuration from the specified class.
    
    db.init_app(app)  # Initialize the SQLAlchemy extension with the app.
    migrate.init_app(app, db)  # Initialize the Flask-Migrate extension with the app and the database.
    login.init_app(app)  # Initialize the Flask-Login extension with the app.
    
    # Set the folder for uploaded files and maximum upload size.
    app.config["UPLOAD_FOLDER"] = os.path.join(app.static_folder, "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024  # 4 MB limit for uploaded files.
    
    # Import models to ensure they are registered with SQLAlchemy.
    from app.models import User, Send, Reply

    # Register the main blueprint for the application.
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')
    
    # Register the API blueprint for the application.
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    
    @app.shell_context_processor
    def make_shell_context():

        return {'db': db, 'User': User, 'Send': Send, 'Reply': Reply}
    
    return app  # Return the configured Flask application.

