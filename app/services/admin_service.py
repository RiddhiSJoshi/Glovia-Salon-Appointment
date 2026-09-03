
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user_model import User, UserRole
from app.repositories.admin_repo import AdminRepository
from app.schemas.admin_schema import (
    AdminUserUpdate,
    SalonOwnerCreate,
)


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

    # ---------------------------------------------------------
    # CREATE SALON OWNER
    # ---------------------------------------------------------

    @staticmethod
    async def create_salon_owner(
        db: AsyncSession,
        data: SalonOwnerCreate,
    ):
        username = data.username.strip().lower()

        # Check whether username already exists
        existing_user = await AdminRepository.get_user_by_username(
            db,
            username,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username is already registered",
            )

        user = User(
            username=username,
            firstname=data.firstname.strip(),
            lastname=data.lastname.strip(),
            password_hash=hash_password(data.password),
            role=UserRole.SALON,
            is_active=True,
        )

        return await AdminRepository.create_user(
            db,
            user,
        )

    # ---------------------------------------------------------
    # UPDATE USER
    # ---------------------------------------------------------

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
            user.firstname = data.firstname.strip()

        if data.lastname is not None:
            user.lastname = data.lastname.strip()

        if data.is_active is not None:
            user.is_active = data.is_active

        if data.role is not None:

            allowed_roles = {
                UserRole.CUSTOMER,
                UserRole.SALON,
                UserRole.ADMIN,
            }

            try:
                new_role = UserRole(data.role.lower())
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid role. Allowed roles: customer, salon, admin",
                )

            if new_role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid role",
                )

            user.role = new_role

        return await AdminRepository.update_user(
            db,
            user,
        )

    # ---------------------------------------------------------
    # DELETE USER
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # STATISTICS
    # ---------------------------------------------------------

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

