from fastapi import APIRouter, Depends

from src.controllers.auth_controller import AuthControlleur
from src.schemas.auth_schema import LoginRequest, TokenResponse, RefreshTokenInput

router = APIRouter(prefix="/auth", tags=["Auth"])



@router.post("/login", response_model=TokenResponse)
def login(
        data: LoginRequest,
        auth_controller: AuthControlleur = Depends()
):
    return auth_controller.login_user(data)


@router.post("/refresh", response_model=TokenResponse)
def refresh_route(data: RefreshTokenInput, auth_controller: AuthControlleur = Depends()):
    return auth_controller.refresh(data)
