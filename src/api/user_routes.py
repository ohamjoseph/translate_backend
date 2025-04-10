from fastapi import APIRouter
from fastapi.params import Depends
from src.controllers.user_controller import UserController
from src.core.security import get_current_user
from src.models.user import User
from src.schemas.user_schema import UserCreate, UserOut


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserOut)
def register_user(
        user: UserCreate,
        user_controller: UserController = Depends()
):
    return user_controller.register_user(user)


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
