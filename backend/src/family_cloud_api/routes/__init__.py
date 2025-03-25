from flask import Blueprint, Flask


def register_api_routes(app: Flask):
    api_blueprint = Blueprint("api", __name__, url_prefix="/api")

    app.register_blueprint(api_blueprint)
