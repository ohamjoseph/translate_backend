from typing import List, Optional

from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.core.dependencies import get_db
from src.models.feedback_model import TranslationFeedback
from src.core.exceptions import DatabaseError


class TranslationFeedbackRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, feedback_data: dict) -> TranslationFeedback:
        try:
            feedback = TranslationFeedback(**feedback_data)
            self.db.add(feedback)
            self.db.commit()
            self.db.refresh(feedback)
            return feedback
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to create feedback: {str(e)}")

    def get_by_id(self, feedback_id: int) -> Optional[TranslationFeedback]:
        return self.db.query(TranslationFeedback).filter(TranslationFeedback.id == feedback_id).first()

    def get_all(
            self,
            skip: int = 0,
            limit: int = 100,
            is_positive: Optional[bool] = None,
            lang_pair: Optional[str] = None
    ) -> List[TranslationFeedback]:
        query = self.db.query(TranslationFeedback)

        if is_positive is not None:
            query = query.filter(TranslationFeedback.is_positive == is_positive)

        if lang_pair:
            source, target = lang_pair.split('-')
            query = query.filter(
                TranslationFeedback.source_lang == source,
                TranslationFeedback.target_lang == target
            )

        return query.offset(skip).limit(limit).all()

    def get_positive_rate(self, lang_pair: Optional[str] = None) -> float:
        query = self.db.query(TranslationFeedback)

        if lang_pair:
            source, target = lang_pair.split('-')
            query = query.filter(
                TranslationFeedback.source_lang == source,
                TranslationFeedback.target_lang == target
            )

        total = query.count()
        if total == 0:
            return 0.0

        positive = query.filter(TranslationFeedback.is_positive == True).count()
        return (positive / total) * 100