"""
Thumbnail generation task for photos and videos
"""

import os
from datetime import datetime, timezone

from PIL import Image
import subprocess
import logging

from src.family_cloud_api.celery import celery
from src.family_cloud_api.database import db
from src.family_cloud_api.models import File
from config import config

logger = logging.getLogger(__name__)

THUMBNAIL_SIZE = (300, 300)
THUMBNAIL_FORMAT = "JPEG"


def get_app():
    """Get Flask app instance for celery tasks"""
    from app import family_cloud_app
    return family_cloud_app


@celery.task(bind=True)
def generate_thumbnail(self, file_path: str, file_id: int, media_type: str = "photo", task_id: str = None):
    """
    Generate and save thumbnail for uploaded file.
    
    Args:
        file_path: Path to original file
        file_id: ID of File record in database
        media_type: Type of media ('photo' or 'video')
        task_id: Upload task ID for status tracking
    """
    from src.family_cloud_api.status import get_status, UploadStatus
    
    try:
        app = get_app()
        with app.app_context():
            file_record = File.query.get(file_id)
            if not file_record:
                logger.error(f"File record {file_id} not found")
                if task_id:
                    status = get_status(task_id)
                    if status:
                        status.status = UploadStatus.COMPLETE
                        status.save()
                return {'status': 'error', 'message': 'File record not found'}

            thumbnail_filename = f"{file_record.id}_thumb.jpg"
            thumbnail_path = os.path.join(config.THUMBNAILS_FOLDER, thumbnail_filename)

            if media_type == "video":
                _generate_video_thumbnail(file_path, thumbnail_path)
            else:  # photo
                _generate_photo_thumbnail(file_path, thumbnail_path)

            # Update database record
            file_record.thumbnail_path = thumbnail_path
            db.session.commit()

            # Update status
            if task_id:
                status = get_status(task_id)
                if status:
                    status.status = UploadStatus.COMPLETE
                    status.save()

            logger.info(f"Thumbnail generated for file {file_id}: {thumbnail_path}")
            return {'status': 'success', 'thumbnail_path': thumbnail_path}

    except Exception as e:
        logger.exception(f"Error generating thumbnail for file {file_id}: {str(e)}")
        if task_id:
            from src.family_cloud_api.status import get_status, UploadStatus
            status = get_status(task_id)
            if status:
                status.status = UploadStatus.ERROR
                status.error = str(e)
                status.save()
        return {'status': 'error', 'message': str(e)}


def _generate_photo_thumbnail(photo_path: str, output_path: str):
    """Generate thumbnail from photo using Pillow"""
    try:
        with Image.open(photo_path) as img:
            # Convert RGBA to RGB if needed
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background

            # Create thumbnail
            img.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)

            # Pad to exact size if needed
            if img.size != THUMBNAIL_SIZE:
                padded = Image.new('RGB', THUMBNAIL_SIZE, (255, 255, 255))
                offset = ((THUMBNAIL_SIZE[0] - img.size[0]) // 2,
                         (THUMBNAIL_SIZE[1] - img.size[1]) // 2)
                padded.paste(img, offset)
                img = padded

            img.save(output_path, THUMBNAIL_FORMAT, quality=85)

    except Exception as e:
        logger.error(f"Error generating photo thumbnail: {str(e)}")
        raise


def _generate_video_thumbnail(video_path: str, output_path: str):
    """
    Generate thumbnail from video by extracting a frame using ffmpeg.
    Extracts frame at 10% into the video for better content preview.
    """
    try:
        # Get video duration first
        duration_cmd = [
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1:nokey=1', video_path
        ]
        result = subprocess.run(duration_cmd, capture_output=True, text=True, timeout=30)
        duration = float(result.stdout.strip())
        
        # Seek to 10% into video
        seek_time = max(1, int(duration * 0.1))  # At least 1 second in

        # Extract frame
        extract_cmd = [
            'ffmpeg', '-ss', str(seek_time), '-i', video_path,
            '-vf', f'scale={THUMBNAIL_SIZE[0]}:{THUMBNAIL_SIZE[1]}:force_original_aspect_ratio=decrease,pad={THUMBNAIL_SIZE[0]}:{THUMBNAIL_SIZE[1]}:(ow-iw)/2:(oh-ih)/2',
            '-vframes', '1', '-q:v', '5',
            '-y', output_path  # Overwrite output
        ]
        subprocess.run(extract_cmd, capture_output=True, timeout=60, check=True)

        logger.info(f"Video thumbnail extracted at {seek_time}s: {output_path}")

    except subprocess.TimeoutExpired:
        logger.error("ffmpeg/ffprobe timeout while generating video thumbnail")
        raise
    except Exception as e:
        logger.error(f"Error generating video thumbnail: {str(e)}")
        raise
