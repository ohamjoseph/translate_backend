from typing import Optional, List
from fastapi.params import Depends
from sqlalchemy.orm import Session
from src.core.dependencies import get_db
from src.core.exceptions import DatabaseError
from src.models.roles import Role


class RoleRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Role]:
        """Get all roles with pagination support"""
        try:
            return self.db.query(Role).offset(skip).limit(limit).all()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch roles: {str(e)}")

    def get_by_id(self, role_id: str) -> Optional[Role]:
        """Get a role by ID with error handling"""
        try:
            return self.db.query(Role).filter(Role.id == role_id).first()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch role by ID: {str(e)}")

    def get_by_name(self, name: str, case_sensitive: bool = False) -> Optional[Role]:
        """Get a role by name with case sensitivity option"""
        try:
            if case_sensitive:
                return self.db.query(Role).filter(Role.name == name).first()
            return self.db.query(Role).filter(Role.name.ilike(name)).first()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch role by name: {str(e)}")

    def create(self, role: Role) -> Role:
        """Create a new role with transaction safety"""
        try:
            self.db.add(role)
            self.db.commit()
            self.db.refresh(role)
            return role
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to create role: {str(e)}")

    def update(self, role: Role, name: str) -> Role:
        """Update an existing role with validation"""
        try:
            role.name = name
            self.db.commit()
            self.db.refresh(role)
            return role
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to update role: {str(e)}")

    def delete(self, role: Role) -> bool:
        """Delete a role and return success status"""
        try:
            self.db.delete(role)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to delete role: {str(e)}")

    def is_role_assigned(self, role_id: str) -> bool:
        """Check if any user has this role assigned"""
        from src.models.user import User  # Avoid circular import
        try:
            return self.db.query(User).filter(User.roles.any(id=role_id)).count() > 0
        except Exception as e:
            raise DatabaseError(f"Failed to check role assignment: {str(e)}")

    def assign_to_user(self, user_id: str, role_id: str) -> bool:
        """Assign a role to a user"""
        from src.models.user import User
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            role = self.get_by_id(role_id)

            if not user or not role:
                return False

            if role not in user.roles:
                user.roles.append(role)
                self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to assign role: {str(e)}")

    def revoke_from_user(self, user_id: str, role_id: str) -> bool:
        """Revoke a role from a user"""
        from src.models.user import User
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            role = self.get_by_id(role_id)

            if not user or not role:
                return False

            if role in user.roles:
                user.roles.remove(role)
                self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to revoke role: {str(e)}")