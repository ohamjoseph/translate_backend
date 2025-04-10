from fastapi import HTTPException
from fastapi.params import Depends

from src.core.exceptions import raise_http
from src.schemas.auth_schema import LoginRequest, TokenResponse, RefreshTokenInput
from src.services.auth_service import AuthService
from src.tracing.audit import log_error


class AuthControlleur:
    def __init__(self, auth_service: AuthService=Depends()):
        self.auth_service = auth_service

    def login_user(self, data: LoginRequest) -> TokenResponse:
        try:
            user = self.auth_service.login(data.email, data.password)
            return TokenResponse(access_token=user['access_token'], refresh_token=user['refresh_token'])
        except HTTPException:
            raise
        except Exception as e:
            log_error("Erreur lors de la tentative de connexion", e)
            raise HTTPException(status_code=500, detail="Erreur interne.")

    def refresh(self, data: RefreshTokenInput) -> TokenResponse:
        try:

            tokens = self.auth_service.refresh_access_token(data.refresh_token)
            return TokenResponse(**tokens)
        except HTTPException:
            raise
        except Exception as e:
            raise raise_http(500, f"Erreur lors du renouvellement du token : {str(e)}")



