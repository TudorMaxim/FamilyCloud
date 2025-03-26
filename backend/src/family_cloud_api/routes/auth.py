from flask import Blueprint, jsonify, request
from flask_login import login_required, login_user, logout_user
from pydantic import ValidationError

from src.family_cloud_api.models import User
from src.family_cloud_api.schemas import LoginCredentials, RegistrationData, UserBaseDTO

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["POST"])
def login():
    try:
        credentials = LoginCredentials(**request.form.to_dict())
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
        return jsonify({"error": e.errors()}), 401


@auth_blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})


@auth_blueprint.route("/register", methods=["POST"])
def register():
    try:
        data = RegistrationData(**request.form)
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
        return jsonify({"message": "Account created successfully."})
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 401
