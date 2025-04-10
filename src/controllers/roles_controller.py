from fastapi import Depends, status
from typing import List
from src.schemas.roles_schema import RoleOut, RoleCreate, RoleUpdate
from src.services.role_service import RoleService
from src.core.exceptions import raise_http

class RoleController:
    def __init__(self, role_service: RoleService = Depends()):
        """Initialize with dependency injection"""
        self.role_service = role_service

    def list(self) -> List[RoleOut]:
        """List all roles with proper error handling"""
        try:
            return self.role_service.list_roles()
        except Exception as e:
            raise raise_http(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Failed to retrieve roles",
                error_type="database_error",
                details={"error": str(e)}
            )

    def create(self, data: RoleCreate) -> RoleOut:
        """Create a new role with validation"""
        try:
            role = self.role_service.create_role(data)
            return RoleOut.model_validate(role)
        except ValueError as e:
            raise raise_http(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e),
                error_type="validation_error"
            )
        except Exception as e:
            raise raise_http(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Failed to create role",
                error_type="database_error",
                details={"error": str(e)}
            )

    def update(self, role_id: str, data: RoleUpdate) -> RoleOut:
        """Update an existing role"""
        try:
            role = self.role_service.update_role(role_id, data)
            return RoleOut.model_validate(role)
        except ValueError as e:
            raise raise_http(
                status_code=status.HTTP_404_NOT_FOUND if "not found" in str(e).lower()
                else status.HTTP_400_BAD_REQUEST,
                message=str(e),
                error_type="not_found" if "not found" in str(e).lower()
                else "validation_error"
            )
        except Exception as e:
            raise raise_http(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Failed to update role",
                error_type="database_error",
                details={"error": str(e)}
            )

    def delete(self, role_id: str) -> dict:
        """Delete a role"""
        try:
            self.role_service.delete_role(role_id)
            return {"message": "Rôle supprimé avec succès"}
        except ValueError as e:
            raise raise_http(
                status_code=status.HTTP_404_NOT_FOUND if "not found" in str(e).lower()
                else status.HTTP_400_BAD_REQUEST,
                message=str(e),
                error_type="not_found" if "not found" in str(e).lower()
                else "validation_error"
            )
        except Exception as e:
            raise raise_http(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Failed to delete role",
                error_type="database_error",
                details={"error": str(e)}
            )

    def get_role(self, role_id: str) -> RoleOut:
        """Get a single role by ID"""
        try:
            role = self.role_service.get_role(role_id)
            if not role:
                raise raise_http(
                    status_code=status.HTTP_404_NOT_FOUND,
                    message="Rôle non trouvé",
                    error_type="not_found"
                )
            return role
        except Exception as e:
            raise raise_http(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Failed to retrieve role",
                error_type="database_error",
                details={"error": str(e)}
            )