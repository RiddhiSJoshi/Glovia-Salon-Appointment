from fastapi import APIRouter, Depends

from app.dependencies import require_roles
from app.models.user import User, UserRole


router = APIRouter(
    tags=["Users"],
)


@router.get("/customer/dashboard")
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