from flask import Blueprint, Flask

from .upload import upload_blueprint


def register_api_routes(app: Flask):
    api_blueprint = Blueprint("api", __name__, url_prefix="/api")

    api_blueprint.register_blueprint(upload_blueprint, url_prefix="/upload")

    app.register_blueprint(api_blueprint)
