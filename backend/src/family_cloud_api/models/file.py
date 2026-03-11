from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.family_cloud_api.database import db


class MediaType(str, Enum):
    PHOTO = "photo"
    VIDEO = "video"


class File(db.Model):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    media_type = Column(String, nullable=False, default=MediaType.PHOTO)
    thumbnail_path = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)  # Duration in seconds for videos
    uploaded_at = Column(DateTime, default=datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="files")
