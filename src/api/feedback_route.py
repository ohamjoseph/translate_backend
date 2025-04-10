from fastapi import APIRouter, Depends, Request, Query
from typing import List, Optional
from src.controllers.feedback_controller import TranslationFeedbackController
from src.models.user import User
from src.schemas.feedback_schema import TranslationFeedbackCreate, TranslationFeedbackOut
from src.core.security import get_current_user_optional

router = APIRouter(
    prefix="/translation-feedback",
    tags=["Translation Feedback"]
)

@router.post("/", response_model=TranslationFeedbackOut, status_code=201)
async def submit_feedback(
    feedback: TranslationFeedbackCreate,
    request: Request,
    controller: TranslationFeedbackController = Depends(),
    current_user=Depends(get_current_user_optional)
):
    return controller.create(feedback, request, current_user)

@router.get("/stats")
async def get_feedback_stats(
    lang_pair: Optional[str] = Query(None),
    controller: TranslationFeedbackController = Depends()
):
    return controller.get_stats(lang_pair)

@router.get("/", response_model=List[TranslationFeedbackOut])
async def get_feedbacks(
    skip: int = 0,
    limit: int = 100,
    is_positive: Optional[bool] = None,
    lang_pair: Optional[str] = Query(None),
    controller: TranslationFeedbackController = Depends()
):
    return controller.get_feedbacks(
        skip=skip,
        limit=limit,
        is_positive=is_positive,
        lang_pair=lang_pair
    )