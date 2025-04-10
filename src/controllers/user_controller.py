from fastapi import HTTPException
from fastapi.params import Depends
from src.schemas.user_schema import UserCreate, UserOut
from src.services.user_service import UserService
from src.core.dependencies import get_db

class UserController:
    def __init__(self, user_service: UserService=Depends()):
        self.user_service = user_service

    def register_user(self, user_data: UserCreate) -> UserOut:
        try:
            user = self.user_service.register_user(user_data)
            return UserOut.model_validate(user)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
