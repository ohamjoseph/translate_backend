from typing import List

from pydantic import BaseModel, EmailStr

from src.schemas.roles_schema import UserRole


class LanguageBase(BaseModel):
    code: str
    name: str

    model_config = {
        "from_attributes": True
    }


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None

class UserOut(BaseModel):
    id: str
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool
    roles: List[UserRole] = []

    model_config = {
        "from_attributes": True
    }
