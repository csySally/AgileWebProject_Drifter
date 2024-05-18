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
    CORS(app)
    
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    app.config["UPLOAD_FOLDER"] = os.path.join(app.static_folder, "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024
    
    from app.models import User, Send, Reply

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Send': Send, 'Reply': Reply}
    
    return app

