from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.family_cloud_api.database import db


class File(db.Model):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="files")
