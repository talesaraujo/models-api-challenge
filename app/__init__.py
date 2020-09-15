from flask import Flask
from flask_migrate import Migrate
from .model import configure as config_db
from .serializer import configure as config_ma
from app.config import Config


def create_app():
    # Create Flask application
    app = Flask(__name__)
    # Import configs
    app.config.from_object(Config)
    # Bind ORM to application
    config_db(app)
    # Configure object serializer
    config_ma(app)
    # Perform db migrations
    Migrate(app, app.db)

    from .routes import bp_aimodels
    # Assign routes blueprint
    app.register_blueprint(bp_aimodels)

    return app  
