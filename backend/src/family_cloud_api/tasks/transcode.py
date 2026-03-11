"""
Video transcoding task to convert videos to MP4 format
"""

import os
import subprocess
import logging
import json

from src.family_cloud_api.celery import celery
from src.family_cloud_api.database import db
from src.family_cloud_api.models import File
from config import config

logger = logging.getLogger(__name__)

# FFmpeg codec settings for optimal compatibility and size
FFMPEG_VIDEO_CODEC = "libx264"
FFMPEG_AUDIO_CODEC = "aac"
FFMPEG_VIDEO_BITRATE = "2000k"  # 2 Mbps - good quality, reasonable file size
FFMPEG_AUDIO_BITRATE = "128k"


def get_app():
    """Get Flask app instance for celery tasks"""
    from app import family_cloud_app
    return family_cloud_app


@celery.task(bind=True)
def transcode_video(self, file_path: str, file_id: int, task_id: str = None):
    """
    Transcode video to MP4 H.264 format for web compatibility.
    Updates File record with processed path and duration.
    
    Args:
        file_path: Path to original video file
        file_id: ID of File record in database
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

            # Generate output filename
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_filename = f"{file_record.id}_processed.mp4"
            output_path = os.path.join(config.PROCESSED_FOLDER, output_filename)

            # Transcode video with progress reporting
            _transcode_with_ffmpeg(file_path, output_path)

            # Extract duration metadata
            duration = _get_video_duration(output_path)

            # Update database record
            file_record.file_path = output_path  # Use processed video as main file
            file_record.duration = duration
            db.session.commit()

            # Update status
            if task_id:
                status = get_status(task_id)
                if status:
                    status.status = UploadStatus.COMPLETE
                    status.save()

            logger.info(f"Video transcoded for file {file_id}: {output_path} (duration: {duration}s)")
            return {
                'status': 'success',
                'file_path': output_path,
                'duration': duration
            }

    except Exception as e:
        logger.exception(f"Error transcoding video for file {file_id}: {str(e)}")
        if task_id:
            status = get_status(task_id)
            if status:
                status.status = UploadStatus.ERROR
                status.error = str(e)
                status.save()
        return {'status': 'error', 'message': str(e)}


def _transcode_with_ffmpeg(input_path: str, output_path: str):
    """
    Transcode video to MP4 using ffmpeg.
    H.264 video codec provides excellent compatibility across browsers.
    """
    try:
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-c:v', FFMPEG_VIDEO_CODEC,  # H.264
            '-b:v', FFMPEG_VIDEO_BITRATE,
            '-preset', 'medium',  # Balance between speed and compression
            '-c:a', FFMPEG_AUDIO_CODEC,  # AAC audio
            '-b:a', FFMPEG_AUDIO_BITRATE,
            '-movflags', '+faststart',  # Enable streaming (seek before download finishes)
            '-y',  # Overwrite output file
            output_path
        ]

        logger.info(f"Starting transcode: {input_path} -> {output_path}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)

        if result.returncode != 0:
            logger.error(f"FFmpeg transcode failed: {result.stderr}")
            raise Exception(f"Transcode failed: {result.stderr}")

        logger.info(f"Transcode completed: {output_path}")

    except subprocess.TimeoutExpired:
        logger.error(f"Transcode timeout for {input_path}")
        raise Exception("Transcode timeout (exceeded 1 hour)")
    except Exception as e:
        logger.error(f"Error during transcode: {str(e)}")
        # Clean up partial output file
        if os.path.exists(output_path):
            os.remove(output_path)
        raise


def _get_video_duration(video_path: str) -> int:
    """Extract video duration in seconds using ffprobe"""
    try:
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        duration = float(result.stdout.strip())
        return int(duration)
    except Exception as e:
        logger.warning(f"Could not extract video duration: {str(e)}")
        return 0
