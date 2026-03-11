"""
File API routes for retrieval and metadata
"""

import logging

from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from src.family_cloud_api.database import db
from src.family_cloud_api.models import File

logger = logging.getLogger(__name__)
file_blueprint = Blueprint("files", __name__)


@file_blueprint.route("/files", methods=["GET"])
@login_required
def get_user_files():
    """
    Get all files uploaded by current user with metadata
    """
    try:
        logger.info(f"Fetching files for user_id={current_user.id}")
        files = File.query.filter_by(user_id=current_user.id).all()
        logger.info(f"Found {len(files)} files for user_id={current_user.id}")

        file_data = [
            {
                "id": f.id,
                "filename": f.filename,
                "media_type": f.media_type,
                "thumbnail_path": f.thumbnail_path,
                "duration": f.duration,
                "uploaded_at": f.uploaded_at.isoformat() if f.uploaded_at else None,
            }
            for f in files
        ]

        return jsonify(file_data), 200
    except Exception as e:
        logger.exception(
            f"Error fetching files for user_id={current_user.id}: {str(e)}"
        )
        return jsonify({"error": str(e)}), 500


@file_blueprint.route("/files/<int:file_id>", methods=["GET"])
@login_required
def get_file_metadata(file_id: int):
    """
    Get metadata for a specific file
    """
    try:
        file_record = File.query.filter_by(id=file_id, user_id=current_user.id).first()

        if not file_record:
            return jsonify({"error": "File not found"}), 404

        metadata = {
            "id": file_record.id,
            "filename": file_record.filename,
            "media_type": file_record.media_type,
            "thumbnail_path": file_record.thumbnail_path,
            "duration": file_record.duration,
            "uploaded_at": (
                file_record.uploaded_at.isoformat() if file_record.uploaded_at else None
            ),
        }

        return jsonify(metadata), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@file_blueprint.route("/files/<int:file_id>", methods=["DELETE"])
@login_required
def delete_file(file_id: int):
    """
    Delete a file and its associated thumbnail
    """
    import os

    from config import config

    try:
        file_record = File.query.filter_by(id=file_id, user_id=current_user.id).first()

        if not file_record:
            return jsonify({"error": "File not found"}), 404

        # Delete file and thumbnail
        if os.path.exists(file_record.file_path):
            os.remove(file_record.file_path)

        if file_record.thumbnail_path and os.path.exists(file_record.thumbnail_path):
            os.remove(file_record.thumbnail_path)

        # Delete database record
        db.session.delete(file_record)
        db.session.commit()

        return jsonify({"message": "File deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
