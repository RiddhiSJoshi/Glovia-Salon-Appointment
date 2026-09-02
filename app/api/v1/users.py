from fastapi import APIRouter, Depends

from app.dependencies import require_roles
from app.models.user_model import User, UserRole


router = APIRouter(
    tags=["Users"],
)

@router.get("/customer")
async def customer_dashboard(
    current_user: User = Depends(
        require_roles(UserRole.CUSTOMER)
    ),
):
    return {
        "message": "Welcome to Customer Dashboard",
        "user_id": current_user.id,
        "role": current_user.role.value,
    }


@router.get("/salon")
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


@router.get("/admin")
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