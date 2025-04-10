from pydantic import BaseModel


class UserRole(BaseModel):
    name: str

    class Config:
        from_attributes = True


class RoleCreate(BaseModel):
    name: str

class RoleUpdate(BaseModel):
    name: str

class RoleOut(BaseModel):
    id: str
    name: str

    model_config = {
        "from_attributes": True
    }