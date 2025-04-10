from fastapi.params import Depends
from jose import jwt, JWTError
from src.core.exceptions import raise_http
from src.core.security import create_access_token, create_refresh_token
from src.core.config import settings
from src.core.utils.password_hash import verify_password
from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.tracing.audit import logger


class AuthService:
    def __init__(self, user_repo: UserRepository=Depends()):
        self.user_repo = user_repo

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.user_repo.get_user_by_email(email)
        if not user:
            raise raise_http(401, "Adresse e-mail non reconnue.")
        if not verify_password(password, user.hashed_password):
            raise raise_http(401, "Mot de passe incorrect.")
        if not user.is_active:
            raise raise_http(403, "Compte désactivé. Contactez un administrateur.")

        return user

    def login(self, email: str, password: str) -> dict:
        user = self.authenticate_user(email, password)
        payload = {"sub": str(user.id)}
        return {
            "access_token": create_access_token(payload),
            "refresh_token": create_refresh_token(payload)
        }

    def refresh_access_token(self, refresh_token: str) -> dict:
        try:
            payload = jwt.decode(refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            if not user_id:
                logger.warning("Tentative avec un Refresh token expiré")
                raise raise_http(401, "Refresh token invalide.")
        except JWTError:
            logger.warning("Tentative avec un Refresh token expiré ou corrompu.")
            raise raise_http(401, "Refresh token expiré ou corrompu.")

        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            logger.warning("Utilisateur introuvable.")
            raise raise_http(404, "Utilisateur introuvable.")
        if not user.is_active:
            logger.warning("Compte désactivé.")
            raise raise_http(403, "Compte désactivé.")


        new_payload = {"sub": str(user.id)}

        
        logger.info("Nouveau token via refresh token")
        return {
            "access_token": create_access_token(new_payload),
            "refresh_token": create_refresh_token(new_payload)
        }
