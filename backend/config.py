import os

import dotenv

dotenv.load_dotenv()


class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", default="development")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", default=".\\uploads")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    SECRET_KEY = os.getenv("SECRET_KEY")
    CLIENT_APP_URL = os.getenv("CLIENT_APP_URL", default="http://localhost:5173")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


config = DevelopmentConfig

if os.getenv("FLASK_ENV") == "production":
    config = ProductionConfig
elif os.getenv("FLASK_ENV") == "test":
    config = TestConfig
