from fastapi import APIRouter
from src.core.permissions import has_permission

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard")
def admin_dashboard(user=has_permission("admin")):
    return {"message": f"Bienvenue {user.full_name}, accès admin validé"}
