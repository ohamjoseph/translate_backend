from typing import List, Optional

from fastapi.params import Depends

from src.core.exceptions import raise_http
from src.models.roles import Role
from src.models.user import User
from src.repositories.role_repository import RoleRepository
from src.schemas.roles_schema import RoleCreate, RoleUpdate


class RoleService:
    def __init__(self, role_repo: RoleRepository=Depends()):
        self.role_repo = role_repo

    def user_has_role(self, user: User, role_name: str) -> bool:
        """Check if user has a specific role"""
        if not user.roles:
            return False
        return any(role.name.lower() == role_name.lower() for role in user.roles)

    def user_has_any_role(self, user: User, role_names: List[str]) -> bool:
        """Check if user has any of the specified roles"""
        if not user.roles:
            return False
        user_roles = {role.name.lower() for role in user.roles}
        return any(role.lower() in user_roles for role in role_names)

    def list_roles(self) -> List[Role]:
        """List all available roles"""
        return self.role_repo.get_all()

    def get_role(self, role_id: str) -> Optional[Role]:
        """Get a specific role by ID"""
        return self.role_repo.get_by_id(role_id)

    def get_role_by_name(self, name: str) -> Optional[Role]:
        """Get a role by its name (case-insensitive)"""
        return self.role_repo.get_by_name(name.lower())

    def create_role(self, data: RoleCreate) -> Role:
        """Create a new role"""
        if self.role_repo.get_by_name(data.name.lower()):
            raise raise_http(409, "Un rôle avec ce nom existe déjà.")

        # Validate role name format if needed
        if not data.name.strip():
            raise raise_http(400, "Le nom du rôle ne peut pas être vide.")

        return self.role_repo.create(Role(name=data.name.strip()))

    def update_role(self, role_id: str, data: RoleUpdate) -> Role:
        """Update an existing role"""
        role = self.role_repo.get_by_id(role_id)
        if not role:
            raise raise_http(404, "Rôle non trouvé.")

        # Check if new name already exists
        existing_role = self.role_repo.get_by_name(data.name.lower())
        if existing_role and existing_role.id != role_id:
            raise raise_http(409, "Un autre rôle avec ce nom existe déjà.")

        return self.role_repo.update(role, data.name.strip())

    def delete_role(self, role_id: str) -> bool:
        """Delete a role"""
        role = self.role_repo.get_by_id(role_id)
        if not role:
            raise raise_http(404, "Rôle non trouvé.")

        # Check if role is assigned to users before deletion
        if self.role_repo.is_role_assigned(role_id):
            raise raise_http(400, "Impossible de supprimer un rôle assigné à des utilisateurs.")

        return self.role_repo.delete(role)

    def assign_role_to_user(self, user: User, role_name: str) -> User:
        """Assign a role to a user"""
        role = self.role_repo.get_by_name(role_name.lower())
        if not role:
            raise raise_http(404, "Rôle non trouvé.")

        if self.user_has_role(user, role_name):
            raise raise_http(400, "L'utilisateur possède déjà ce rôle.")

        return self.role_repo.assign_role(user, role)

    def revoke_role_from_user(self, user: User, role_name: str) -> User:
        """Remove a role from a user"""
        if not self.user_has_role(user, role_name):
            raise raise_http(400, "L'utilisateur ne possède pas ce rôle.")

        return self.role_repo.revoke_role(user, role_name.lower())
