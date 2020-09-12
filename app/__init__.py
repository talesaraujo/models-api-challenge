from flask import Flask
from flask_migrate import Migrate
from .model import configure as config_db
from .serializer import configure as config_ma
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    

    # Import configs
    app.config.from_object(Config)

    config_db(app)
    config_ma(app)

    Migrate(app, app.db)

    from .main import bp_aimodels
    app.register_blueprint(bp_aimodels)

    return app  
