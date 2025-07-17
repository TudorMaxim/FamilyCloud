from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from pydantic import ValidationError

from src.family_cloud_api.models import User
from src.family_cloud_api.schemas import LoginCredentials, RegistrationData, UserBaseDTO

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["POST"])
def login():
    try:
        credentials = LoginCredentials(**request.get_json())
        user = User.query.filter_by(email=credentials.email).first()

        if not user:
            return (
                jsonify(
                    {"error": f"User with email {credentials.email} does not exist."}
                ),
                404,
            )

        if user.check_password(credentials.password):
            login_user(user)
            return jsonify(
                {
                    "message": "Login successful",
                    "user": UserBaseDTO(**user.to_dict()).model_dump(),
                }
            )

        return jsonify({"error": "Invalid password"}), 401
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400


@auth_blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})


@auth_blueprint.route("/register", methods=["POST"])
def register():
    try:
        data = RegistrationData(**request.get_json())
        if User.query.filter_by(email=data.email).first():
            return (
                jsonify({"error": f"User with email {data.email} already exists."}),
                401,
            )

        User.create(
            first_name=data.firstName,
            last_name=data.lastName,
            email=data.email,
            password=data.password,
        )
        return jsonify({"message": "Account created successfully"})
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400


@auth_blueprint.route("/me", methods=["GET"])
def me():
    if current_user.is_authenticated:
        return (
            jsonify(
                {
                    "email": current_user.email,
                    "id": current_user.id,
                    "firstName": current_user.first_name,
                    "lastName": current_user.last_name,
                }
            ),
            200,
        )
    return jsonify({"message": "Not authenticated"}), 401
