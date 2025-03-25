import os

from flask import Flask
from flask_cors import CORS

from config import config

from .celery import setup_celery
from .database import db, migrate
from .routes import register_api_routes


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)
    register_api_routes(app)
    setup_celery()

    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload folder exists

    db.init_app(app)
    import src.family_cloud_api.models  # Register models for alembic to handle migrations

    migrate.init_app(app, db)

    return app
