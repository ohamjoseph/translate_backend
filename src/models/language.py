from sqlalchemy import Column, String

from src.core.database import Base


class Language(Base):
    __tablename__ = "languages"

    code = Column(String, primary_key=True)  # ex: 'moore', 'fr', 'en'
    name = Column(String, nullable=False)
