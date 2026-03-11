"""
Upload process status tracking
Tracks progress through: uploading -> thumbnail generation -> transcoding (if video) -> complete
"""

import json
from typing import Optional

# Try to use Redis for distributed tracking, fall back to in-memory dict
try:
    import redis

    from config import config

    redis_client = (
        redis.from_url(config.CELERY_RESULT_BACKEND)
        if hasattr(config, "CELERY_RESULT_BACKEND")
        else None
    )
except Exception:
    redis_client = None

# In-memory fallback
_status_cache = {}


class UploadStatus:
    """Track upload process status"""

    UPLOADING = "uploading"
    GENERATING_THUMBNAIL = "thumbnail"
    TRANSCODING = "transcoding"
    COMPLETE = "complete"
    ERROR = "error"

    def __init__(self, task_id: str, filename: str, media_type: str):
        self.task_id = task_id
        self.filename = filename
        self.media_type = media_type
        self.status = self.UPLOADING
        self.progress = 0
        self.error = None
        self.file_id = None

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "filename": self.filename,
            "media_type": self.media_type,
            "status": self.status,
            "progress": self.progress,
            "error": self.error,
            "file_id": self.file_id,
        }

    def save(self):
        """Persist status to Redis or cache"""
        data = json.dumps(self.to_dict())
        if redis_client:
            try:
                redis_client.setex(f"upload:{self.task_id}", 3600, data)  # 1 hour TTL
            except Exception:
                _status_cache[self.task_id] = self
        else:
            _status_cache[self.task_id] = self

    @staticmethod
    def load(task_id: str) -> Optional["UploadStatus"]:
        """Retrieve status from Redis or cache"""
        if redis_client:
            try:
                data = redis_client.get(f"upload:{task_id}")
                if data:
                    status_dict = json.loads(data)
                    status = UploadStatus(
                        status_dict["task_id"],
                        status_dict["filename"],
                        status_dict["media_type"],
                    )
                    status.status = status_dict["status"]
                    status.progress = status_dict["progress"]
                    status.error = status_dict["error"]
                    status.file_id = status_dict["file_id"]
                    return status
            except Exception:
                pass

        if task_id in _status_cache:
            return _status_cache[task_id]

        return None

    @staticmethod
    def delete(task_id: str):
        """Remove status from tracking"""
        if redis_client:
            try:
                redis_client.delete(f"upload:{task_id}")
            except Exception:
                pass

        _status_cache.pop(task_id, None)


def create_status(task_id: str, filename: str, media_type: str) -> UploadStatus:
    """Create and save a new upload status"""
    status = UploadStatus(task_id, filename, media_type)
    status.save()
    return status


def get_status(task_id: str) -> Optional[UploadStatus]:
    """Get existing upload status"""
    return UploadStatus.load(task_id)
