from typing import List

from pydantic import BaseModel, EmailStr

from src.schemas.roles_schema import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class UserOut(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None = None
    is_active: bool
    roles: List[UserRole] = []

    model_config = {
        "from_attributes": True
    }
