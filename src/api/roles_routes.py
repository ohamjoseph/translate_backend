from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.controllers.roles_controller import RoleController
from src.schemas.roles_schema import RoleCreate, RoleUpdate, RoleOut
from src.core.exceptions import raise_http

router = APIRouter(
    prefix="/roles",
    tags=["Rôles"],
    responses={
        404: {"description": "Rôle non trouvé"},
        403: {"description": "Opération non autorisée"},
        400: {"description": "Requête invalide"}
    }
)

@router.get(
    "/",
    response_model=List[RoleOut],
    summary="Lister tous les rôles",
    description="Récupère la liste de tous les rôles disponibles"
)
async def list_roles(controller: RoleController = Depends()):
    return controller.list()

@router.post(
    "/",
    response_model=RoleOut,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouveau rôle",
    responses={
        201: {"description": "Rôle créé avec succès"},
        409: {"description": "Un rôle avec ce nom existe déjà"}
    }
)
async def create_role(
    data: RoleCreate,
    controller: RoleController = Depends()
):
    return controller.create(data)

@router.get(
    "/{role_id}",
    response_model=RoleOut,
    summary="Récupérer un rôle spécifique",
    responses={
        200: {"description": "Détails du rôle"},
        404: {"description": "Rôle non trouvé"}
    }
)
async def get_role(
    role_id: str,
    controller: RoleController = Depends()
):
    try:
        return controller.get_role(role_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise raise_http(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Erreur lors de la récupération du rôle",
            error_type="server_error"
        )

@router.put(
    "/{role_id}",
    response_model=RoleOut,
    summary="Mettre à jour un rôle",
    responses={
        200: {"description": "Rôle mis à jour"},
        404: {"description": "Rôle non trouvé"},
        400: {"description": "Données de requête invalides"}
    }
)
async def update_role(
    role_id: str,
    data: RoleUpdate,
    controller: RoleController = Depends()
):
    return controller.update(role_id, data)

@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un rôle",
    responses={
        204: {"description": "Rôle supprimé avec succès"},
        404: {"description": "Rôle non trouvé"},
        400: {"description": "Impossible de supprimer - rôle en cours d'utilisation"}
    }
)
async def delete_role(
    role_id: str,
    controller: RoleController = Depends()
):
    controller.delete(role_id)
    return None