import os

import dotenv

dotenv.load_dotenv()


class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", default="development")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = DevelopmentConfig if Config.FLASK_ENV == "development" else ProductionConfig
