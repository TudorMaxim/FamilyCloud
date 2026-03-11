"""File upload validation utilities for backend"""

from config import config

VALID_PHOTO_EXTENSIONS = {
    ext.lower() for ext in config.FILE_VALIDATION_CONFIG["photos"]["extensions"]
}
VALID_PHOTO_MIME_TYPES = set(config.FILE_VALIDATION_CONFIG["photos"]["mime_types"])
VALID_VIDEO_EXTENSIONS = {
    ext.lower() for ext in config.FILE_VALIDATION_CONFIG["videos"]["extensions"]
}
VALID_VIDEO_MIME_TYPES = set(config.FILE_VALIDATION_CONFIG["videos"]["mime_types"])

MAX_PHOTO_SIZE = config.FILE_VALIDATION_CONFIG["photos"]["max_size_bytes"]
MAX_VIDEO_SIZE = config.FILE_VALIDATION_CONFIG["videos"]["max_size_bytes"]


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    if "." not in filename:
        return ""
    return "." + filename.rsplit(".", 1)[1].lower()


def detect_media_type(filename: str, mime_type: str = "") -> str:
    """Detect media type from filename and MIME type"""
    ext = get_file_extension(filename)

    # Check photos
    if ext in VALID_PHOTO_EXTENSIONS or mime_type in VALID_PHOTO_MIME_TYPES:
        return "photo"

    # Check videos
    if ext in VALID_VIDEO_EXTENSIONS or mime_type in VALID_VIDEO_MIME_TYPES:
        return "video"

    return "invalid"


def validate_file_upload(
    filename: str, file_size: int, mime_type: str = ""
) -> tuple[bool, str | None, str | None]:
    """
    Validate file for upload.
    Returns: (is_valid, error_message, media_type)
    """
    media_type = detect_media_type(filename, mime_type)

    if media_type == "invalid":
        return False, f"Unsupported file type: {filename}", None

    if media_type == "photo":
        if file_size > MAX_PHOTO_SIZE:
            max_size_mb = MAX_PHOTO_SIZE / (1024 * 1024)
            file_size_mb = file_size / (1024 * 1024)
            return (
                False,
                f"Photo too large: {file_size_mb:.2f}MB (max {max_size_mb:.0f}MB)",
                None,
            )
        return True, None, "photo"

    else:  # video
        if file_size > MAX_VIDEO_SIZE:
            max_size_mb = MAX_VIDEO_SIZE / (1024 * 1024)
            file_size_mb = file_size / (1024 * 1024)
            return (
                False,
                f"Video too large: {file_size_mb:.2f}MB (max {max_size_mb:.0f}MB)",
                None,
            )
        return True, None, "video"
