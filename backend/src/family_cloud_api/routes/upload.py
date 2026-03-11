import logging
import os
import uuid

from flask import Blueprint, Response, jsonify, request
from flask_login import current_user, login_required

from config import config
from src.family_cloud_api.status import create_status, get_status
from src.family_cloud_api.tasks import clients, upload
from src.family_cloud_api.validation import validate_file_upload

logger = logging.getLogger(__name__)
upload_blueprint = Blueprint("upload", __name__)


@upload_blueprint.route("/upload", methods=["POST"])
@login_required
def upload_file():
    try:
        f = request.files["file"]
        filename = f.filename
        chunk_index = int(request.form["chunk_index"])
        total_chunks = int(request.form["total_chunks"])
        task_id = request.form.get("task_id", str(uuid.uuid4()))
        media_type = request.form.get("media_type", "")

        logger.info(
            f"Upload chunk: {filename} ({chunk_index}/{total_chunks}), media_type={media_type}, content_type={f.content_type}"
        )

        # Validate file on first chunk
        if chunk_index == 0:
            # For chunked uploads, only validate extension/MIME type on first chunk
            # Size was already validated on client side; content_length here is just the chunk size
            is_valid, error_msg, detected_media_type = validate_file_upload(
                filename,
                0,  # Don't validate size for chunks - already validated client-side
                f.content_type or "",
            )
            if not is_valid:
                logger.warning(f"Validation failed for {filename}: {error_msg}")
                return jsonify({"error": error_msg}), 400

            # Use detected media type if not provided by client
            if not media_type:
                media_type = detected_media_type
                logger.info(f"Detected media type: {media_type}")

            # Create status record
            create_status(task_id, filename, media_type)

        chunk_filename = f"{task_id}_{chunk_index}_{filename}"
        chunk_path = os.path.join(config.CHUNKS_FOLDER, chunk_filename)
        f.save(chunk_path)

        if chunk_index == total_chunks - 1:
            final_path = os.path.join(
                config.UPLOAD_FOLDER, f"{uuid.uuid4().hex}_{filename}"
            )
            chunks_info = [
                {
                    "chunk_path": os.path.join(
                        config.CHUNKS_FOLDER, f"{task_id}_{i}_{filename}"
                    ),
                    "final_path": final_path,
                    "filename": filename,
                }
                for i in range(total_chunks)
            ]
            upload.apply_async(args=[chunks_info, task_id, media_type, current_user.id])
            logger.info(f"Queued assembly task for {filename}")

        return jsonify({"task_id": task_id}), 202

    except Exception as e:
        logger.exception(f"Error in upload_file: {str(e)}")
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500


# SSE endpoint for progress updates
@upload_blueprint.route("/progress/<task_id>")
@login_required
def progress(task_id):
    def event_stream():
        class Writer:
            def __init__(self):
                self.queue = []

            def write(self, data):
                self.queue.append(data)

            def flush(self):
                pass

        w = Writer()
        clients[task_id] = w
        try:
            while True:
                while w.queue:
                    yield w.queue.pop(0)
        finally:
            clients.pop(task_id, None)

    return Response(event_stream(), mimetype="text/event-stream")


@upload_blueprint.route("/status/<task_id>", methods=["GET"])
@login_required
def get_upload_status(task_id):
    """Get current upload status including processing state"""
    status = get_status(task_id)

    if not status:
        return jsonify({"error": "Status not found"}), 404

    return jsonify(status.to_dict()), 200
