from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import uuid
from src.core.database import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)

    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")
