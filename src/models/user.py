from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from src.core.database import Base

user_languages = Table(
    "user_languages",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("language_code", ForeignKey("languages.code"), primary_key=True)
)

# Table de jointure User <-> Role
user_roles = Table(
    "user_roles", Base.metadata,
    Column("user_id", String, ForeignKey("users.id")),
    Column("role_id", String, ForeignKey("roles.id"))
)

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_oauth_user = Column(Boolean, default=False)

    languages = relationship("Language", secondary=user_languages, backref="users")
    bio = Column(Text, nullable=True)  # Courte description ou motivation
    profile_picture_url = Column(String, nullable=True)
    last_active_at = Column(DateTime(timezone=True), nullable=True)

    roles = relationship("Role", secondary=user_roles, back_populates="users")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
