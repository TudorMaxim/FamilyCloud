import os

import dotenv

dotenv.load_dotenv()

# File validation configuration
FILE_VALIDATION_CONFIG = {
    "photos": {
        "extensions": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
        "mime_types": ["image/jpeg", "image/png", "image/gif", "image/webp"],
        "max_size_bytes": 100 * 1024 * 1024,  # 100MB
        "label": "Photo",
    },
    "videos": {
        "extensions": [".mp4", ".mov", ".webm", ".mkv", ".avi"],
        "mime_types": [
            "video/mp4",
            "video/quicktime",
            "video/webm",
            "video/x-msvideo",
            "video/x-matroska",
        ],
        "max_size_bytes": 1024 * 1024 * 1024,  # 1GB
        "label": "Video",
    },
}


class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", default="development")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", default="./uploads")
    CHUNKS_FOLDER = os.getenv("CHUNKS_FOLDER", default="./chunks")
    THUMBNAILS_FOLDER = os.getenv("THUMBNAILS_FOLDER", default="./uploads/thumbnails")
    PROCESSED_FOLDER = os.getenv("PROCESSED_FOLDER", default="./uploads/processed")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    SECRET_KEY = os.getenv("SECRET_KEY")
    CLIENT_APP_URL = os.getenv("CLIENT_APP_URL", default="http://localhost:5173")
    FILE_VALIDATION_CONFIG = FILE_VALIDATION_CONFIG


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
