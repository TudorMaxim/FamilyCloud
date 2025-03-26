import os

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from config import config

from .celery import setup_celery
from .database import db, migrate
from .models import User
from .oauth import oauth
from .routes import register_api_routes

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(config)
    register_api_routes(app)
    setup_celery()

    login_manager.init_app(app)
    oauth.init_app(app)

    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload folder exists

    db.init_app(app)
    import src.family_cloud_api.models  # Register models for alembic to handle migrations

    migrate.init_app(app, db)

    return app
