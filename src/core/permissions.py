from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.dependencies import get_db
from src.core.security import get_current_user
from src.services.role_service import RoleService
from src.repositories.role_repository import RoleRepository

def has_permission(role_name: str):
    def wrapper(user=Depends(get_current_user), db: Session = Depends(get_db)):
        service = RoleService(RoleRepository(db))
        if not service.user_has_role(user, role_name):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission refusée : rôle requis '{role_name}'"
            )
        return user  # facultatif
    return Depends(wrapper)
