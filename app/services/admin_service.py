from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User
from app.repositories.admin_repo import AdminRepository
from app.schemas.admin_schema import AdminUserUpdate


class AdminService:

    @staticmethod
    async def get_users(
        db: AsyncSession,
    ):

        return await AdminRepository.get_users(db)

    @staticmethod
    async def get_user(
        db: AsyncSession,
        user_id: int,
    ):

        user = await AdminRepository.get_user_by_id(
            db,
            user_id,
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    @staticmethod
    async def update_user(
        db: AsyncSession,
        user_id: int,
        data: AdminUserUpdate,
    ):

        user = await AdminService.get_user(
            db,
            user_id,
        )

        if data.firstname is not None:
            user.firstname = data.firstname

        if data.lastname is not None:
            user.lastname = data.lastname

        if data.is_active is not None:
            user.is_active = data.is_active

        if data.role is not None:

            allowed_roles = {
                "customer",
                "salon",
                "admin",
            }

            if data.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid role",
                )

            user.role = data.role

        return await AdminRepository.update_user(
            db,
            user,
        )

    @staticmethod
    async def delete_user(
        db: AsyncSession,
        user_id: int,
    ):

        user = await AdminService.get_user(
            db,
            user_id,
        )

        await AdminRepository.delete_user(
            db,
            user,
        )

    @staticmethod
    async def get_statistics(
        db: AsyncSession,
    ):

        return {
            "total_users":
                await AdminRepository.count_users(db),

            "total_customers":
                await AdminRepository.count_customers(db),

            "total_salon_owners":
                await AdminRepository.count_salon_owners(db),

            "total_admins":
                await AdminRepository.count_admins(db),

            "total_salons":
                await AdminRepository.count_salons(db),

            "total_staff":
                await AdminRepository.count_staff(db),

            "total_services":
                await AdminRepository.count_services(db),

            "total_appointments":
                await AdminRepository.count_appointments(db),

            "total_reviews":
                await AdminRepository.count_reviews(db),
        }