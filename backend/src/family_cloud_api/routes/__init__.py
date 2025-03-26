from flask import Blueprint, Flask

from .auth import auth_blueprint
from .auth_google import auth_google_blueprint
from .upload import upload_blueprint


def register_api_routes(app: Flask):
    api_blueprint = Blueprint("api", __name__, url_prefix="/api")

    api_blueprint.register_blueprint(upload_blueprint)
    api_blueprint.register_blueprint(auth_blueprint)
    api_blueprint.register_blueprint(auth_google_blueprint)

    app.register_blueprint(api_blueprint)
