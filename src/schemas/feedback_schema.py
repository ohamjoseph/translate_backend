from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class TranslationFeedbackBase(BaseModel):
    source_text: str = Field(..., max_length=5000)
    translated_text: str = Field(..., max_length=5000)
    source_lang: str = Field(..., max_length=10)
    target_lang: str = Field(..., max_length=10)
    is_positive: bool
    comments: Optional[str] = Field(None, max_length=1000)
    suggested_translation: Optional[str] = Field(None, max_length=5000)

class TranslationFeedbackCreate(TranslationFeedbackBase):
    is_anonymous: bool = False
    email: Optional[EmailStr] = None
    user_id: Optional[str] = None

class TranslationFeedbackOut(TranslationFeedbackBase):
    id: int
    is_anonymous: bool
    timestamp: datetime
    source_lang: str
    target_lang: str

    class Config:
        from_attributes = True