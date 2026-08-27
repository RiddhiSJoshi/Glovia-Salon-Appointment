from fastapi import APIRouter, Depends

from app.dependencies import require_roles
from app.models.user import User, UserRole


router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Admin"],
)


@router.get("/dashboard")
async def admin_dashboard(
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):

    return {
        "message": "Welcome to Admin Dashboard",
        "user_id": current_user.id,
        "role": current_user.role.value,
    }