from fastapi.params import Depends
from src.schemas.user_schema import UserCreate
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.core.utils.password_hash import get_password_hash
from src.tracing.audit import log_audit_event

class UserService:
    def __init__(self, user_repository: UserRepository=Depends()):
        self.user_repository = user_repository

    def register_user(self, user_data: UserCreate) -> User:
        existing = self.user_repository.get_user_by_email(user_data.email)
        if existing:
            raise ValueError("Email déjà utilisé.")

        hashed = get_password_hash(user_data.password)
        user = User(email=user_data.email, hashed_password=hashed, first_name=user_data.first_name, last_name=user_data.last_name)

        created = self.user_repository.create_user(user)
        log_audit_event(f"Nouvel utilisateur créé : {user.email}")
        return created

    def get_user_by_email(self, email: str) -> User | None:
        return self.user_repository.get_user_by_email(email)

    def get_user_by_id(self, user_id: str) -> User | None:
        return self.user_repository.get_user_by_id(user_id)
