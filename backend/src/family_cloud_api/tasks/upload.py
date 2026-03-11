import json
import logging
import os
from datetime import datetime, timezone

from src.family_cloud_api.celery import celery
from src.family_cloud_api.database import db
from src.family_cloud_api.models import File, MediaType
from src.family_cloud_api.status import UploadStatus, get_status

logger = logging.getLogger(__name__)

clients = {}


def get_app():
    """Get Flask app instance for celery tasks"""
    from app import family_cloud_app

    return family_cloud_app


@celery.task(bind=True)
def upload(
    self, chunks_info, task_id: str, media_type: str = "photo", user_id: int = None
):
    """
    Assemble chunks into final file and create database record.
    Triggers thumbnail and transcode tasks if applicable.
    """
    from src.family_cloud_api.tasks.thumbnails import generate_thumbnail
    from src.family_cloud_api.tasks.transcode import transcode_video

    try:
        total = len(chunks_info)

        for i, info in enumerate(chunks_info):
            chunk_path = info["chunk_path"]
            final_path = info["final_path"]

            with open(final_path, "ab") as out_f, open(chunk_path, "rb") as in_f:
                out_f.write(in_f.read())
            os.remove(chunk_path)

            # Send progress to SSE
            if task_id in clients:
                msg = json.dumps(
                    {"file": info["filename"], "current": i + 1, "total": total}
                )
                clients[task_id].write(f"data: {msg}\n\n")

        # Create app context for database operations
        app = get_app()
        with app.app_context():
            # Create File record
            file_record = File(
                filename=chunks_info[0]["filename"],
                file_path=chunks_info[0]["final_path"],
                media_type=(
                    MediaType.VIDEO if media_type == "video" else MediaType.PHOTO
                ),
                uploaded_at=datetime.now(timezone.utc),
                user_id=user_id,
            )
            db.session.add(file_record)
            db.session.commit()
            file_id = file_record.id
            file_path = file_record.file_path

            logger.info(
                f"File record created: id={file_id}, filename={file_record.filename}, user_id={user_id}, media_type={media_type}"
            )

            # Update status with file ID
            status = get_status(task_id)
            if status:
                status.file_id = file_id

            # Queue thumbnail and transcode tasks
            if media_type == "video":
                # Update status to transcoding
                if status:
                    status.status = UploadStatus.TRANSCODING
                    status.save()

                # Queue transcode task first (video -> MP4)
                transcode_video.apply_async(
                    args=[file_path, file_id, task_id],
                    countdown=2,  # Wait 2 seconds before starting
                )
                # Queue thumbnail task (extract frame from original)
                generate_thumbnail.apply_async(
                    args=[file_path, file_id, "video", task_id], countdown=1
                )
            else:  # photo
                # Update status to thumbnail generation
                if status:
                    status.status = UploadStatus.GENERATING_THUMBNAIL
                    status.save()

                # Queue thumbnail task (generate thumbnail)
                generate_thumbnail.apply_async(
                    args=[file_path, file_id, "photo", task_id], countdown=1
                )

        return {"status": "Completed", "file_id": file_id}

    except Exception as e:
        logger.exception(f"Error in upload task: {str(e)}")
        return {"status": "error", "message": str(e)}
