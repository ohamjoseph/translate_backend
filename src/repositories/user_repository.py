from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.core.dependencies import get_db
from src.models.user import User

class UserRepository:
    def __init__(self, db: Session=Depends(get_db)):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: str) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def list_user(self) -> list[User]:
        return self.db.query(User).all()

    def delete_user(self, user: User):
        self.db.delete(user)
        self.db.commit()
