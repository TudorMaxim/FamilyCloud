from flask import Blueprint, jsonify, url_for
from flask_login import login_user

from src.family_cloud_api import oauth
from src.family_cloud_api.models import User
from src.family_cloud_api.schemas import UserBaseDTO

auth_google_blueprint = Blueprint("auth_google", __name__, url_prefix="/google")


@auth_google_blueprint.route("/login")
def login():
    return oauth.google.authorize_redirect(
        url_for("auth_google_blueprint.google_callback", _external=True)
    )


@auth_google_blueprint.route("/callback")
def google_callback():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.get("userinfo").json()

    email = user_info["email"]
    google_id = user_info["localId"]
    displayName = user_info.get("displayName")

    first_name = None
    last_name = None

    if displayName:
        tokens = displayName.split(" ")
        first_name = tokens[0]
        last_name = tokens[1] if len(tokens) > 1 else None

    existing_user = User.query.filter_by(email=email).first()
    if not existing_user:
        user = User.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=None,
            google_id=google_id,
        )
        login_user(user)
        return jsonify(
            {
                "message": "Login successful",
                "user": UserBaseDTO(**user.to_dict()).model_dump(),
            }
        )

    if not existing_user.google_id:
        return (
            jsonify(
                {
                    "error": "This email is already registered with password authentication."
                }
            ),
            401,
        )

    login_user(existing_user)
    return jsonify(
        {
            "message": "Login successful",
            "user": UserBaseDTO(**user.to_dict()).model_dump(),
        }
    )
