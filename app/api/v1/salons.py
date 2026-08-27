from fastapi import APIRouter, Depends

from app.dependencies import require_roles
from app.models.user import User, UserRole


router = APIRouter(
    prefix="/api/v1/salons",
    tags=["Salons"],
)


@router.get("/dashboard")
async def salon_dashboard(
    current_user: User = Depends(
        require_roles(UserRole.SALON)
    ),
):

    return {
        "message": "Welcome to Salon Dashboard",
        "user_id": current_user.id,
        "role": current_user.role.value,
    }