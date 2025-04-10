from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime
from src.core.database import Base


class TranslationFeedback(Base):
    __tablename__ = "translation_feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=True)  # Nullable for anonymous
    is_anonymous = Column(Boolean, default=False)
    email = Column(String, nullable=True)  # Optional contact for anonymous

    # Translation context
    source_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    source_lang = Column(String(10), nullable=False)
    target_lang = Column(String(10), nullable=False)

    # Feedback details
    is_positive = Column(Boolean, nullable=False)
    comments = Column(Text, nullable=True)  # Additional user comments
    suggested_translation = Column(Text, nullable=True)  # User's suggested alternative

    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45), nullable=True)  # For basic spam prevention
    user_agent = Column(Text, nullable=True)  # Client info