from typing import List, Optional
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from src.services.feedback_service import TranslationFeedbackService
from src.repositories.feedback_repository import TranslationFeedbackRepository
from src.schemas.feedback_schema import TranslationFeedbackCreate, TranslationFeedbackOut
from src.core.dependencies import get_db
from src.models.user import User


class TranslationFeedbackController:
    def __init__(self, service: TranslationFeedbackService=Depends()):
        self.service = service

    def create(
            self,
            feedback: TranslationFeedbackCreate,
            request: Request,
            current_user: Optional[User] = None
    ) -> TranslationFeedbackOut:
        # Set user ID if authenticated and not anonymous
        if current_user and not feedback.is_anonymous:
            feedback.user_id = str(current_user.id)

        feedback = self.service.create_feedback(feedback, request)
        return TranslationFeedbackOut.model_validate(feedback)

    def get_stats(self, lang_pair: Optional[str] = None) -> dict:
        return self.service.get_feedback_stats(lang_pair)

    def get_feedbacks(
            self,
            skip: int = 0,
            limit: int = 100,
            is_positive: Optional[bool] = None,
            lang_pair: Optional[str] = None
    ) -> List[TranslationFeedbackOut]:
        out_feedbacks = self.service.get_feedbacks(skip, limit, is_positive, lang_pair)
        return [TranslationFeedbackOut.model_validate(f) for f in out_feedbacks]