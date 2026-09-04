from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.user_model import User
from app.schemas.admin_schema import (
    AdminStatsResponse,
    AdminUserResponse,
    AdminUserUpdate,
    SalonOwnerCreate
)
from app.services.admin_service import AdminService
from app.core.security import get_current_admin


router = APIRouter(
    tags=["Admin"],
)

@router.get(
    "/users",
    response_model=list[AdminUserResponse],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    return await AdminService.get_users(db)

@router.get(
    "/users/{user_id}",
    response_model=AdminUserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    return await AdminService.get_user(
        db,
        user_id,
    )

@router.put(
    "/users/{user_id}",
    response_model=AdminUserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: int,
    data: AdminUserUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return await AdminService.update_user(
            db,
            user_id,
            data,
        )

@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    await AdminService.delete_user(
        db,
        user_id,
    )

    return None

@router.get(
    "/statistics",
    response_model=AdminStatsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_statistics(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):

    return await AdminService.get_statistics(db)

@router.post(
    "/salon-owners",
    response_model=AdminUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_salon_owner(
    data: SalonOwnerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    return await AdminService.create_salon_owner(
        db,
        data,
    )