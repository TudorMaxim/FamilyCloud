from flask import Flask
from flask_cors import CORS

from config import config

from .database import db, migrate
from .routes import register_api_routes


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)

    db.init_app(app)

    import src.family_cloud_api.models

    migrate.init_app(app, db)

    register_api_routes(app)
    return app
