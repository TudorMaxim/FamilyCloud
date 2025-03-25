from flask import Blueprint, jsonify

from src.family_cloud_api.tasks import upload

upload_blueprint = Blueprint("upload", __name__)


@upload_blueprint.route("/", methods=["POST"])
def upload_file():
    task = upload.apply_async(args=[])

    return (
        jsonify(
            {
                "message": "Files submitted successfully",
                "taskId": task.id,
            }
        ),
        202,
    )
