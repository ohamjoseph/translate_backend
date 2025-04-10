from typing import List, Optional

from fastapi.params import Depends

from src.models.feedback_model import TranslationFeedback
from src.repositories.feedback_repository import TranslationFeedbackRepository
from src.schemas.feedback_schema import TranslationFeedbackCreate, TranslationFeedbackOut
from src.core.exceptions import raise_http
from fastapi import Request


class TranslationFeedbackService:
    def __init__(self, repository: TranslationFeedbackRepository=Depends()):
        self.repository = repository

    def create_feedback(
            self,
            feedback_data: TranslationFeedbackCreate,
            request: Optional[Request] = None
    ) -> TranslationFeedback:
        # Validate anonymous feedback
        # if feedback_data.is_anonymous and not feedback_data.email:
        #     raise raise_http(400, "Email required for anonymous feedback")

        # Prepare additional metadata
        extra_data = {}
        if request:
            extra_data = {
                'ip_address': request.client.host if request.client else None,
                'user_agent': request.headers.get('user-agent')
            }

        # Create the feedback
        db_feedback = self.repository.create({
            **feedback_data.model_dump(),
            **extra_data
        })

        if not db_feedback:
            raise raise_http(400, "Failed to create feedback")

        return db_feedback

    def get_feedback_stats(self, lang_pair: Optional[str] = None) -> dict:
        return {
            "positive_rate": self.repository.get_positive_rate(lang_pair),
            "total_feedbacks": self.repository.get_all(lang_pair=lang_pair, limit=0)
        }

    def get_feedbacks(
            self,
            skip: int = 0,
            limit: int = 100,
            is_positive: Optional[bool] = None,
            lang_pair: Optional[str] = None
    ) -> List[TranslationFeedback]:
        return self.repository.get_all(
            skip=skip,
            limit=limit,
            is_positive=is_positive,
            lang_pair=lang_pair
        )