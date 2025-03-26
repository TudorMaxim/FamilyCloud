from datetime import datetime, timezone

from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src.family_cloud_api.database import db

bcrypt = Bcrypt()


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))
    files = relationship("File", back_populates="owner")

    password_hash = Column(String(256), nullable=True)
    google_id = Column(String(256), unique=True, nullable=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def create(
        first_name: str | None,
        last_name: str | None,
        email: str,
        password: str | None,
        google_id: str | None = None,
    ):
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            google_id=google_id,
        )

        if password:
            user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return user

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
