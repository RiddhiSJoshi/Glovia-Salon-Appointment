from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon_model import Staff
from app.repositories.salon_repo import SalonRepository
from app.repositories.staff_repo import StaffRepository
from app.schemas.staff_schema import (
    StaffCreate,
    StaffUpdate,
)


class StaffService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.salon_repo = SalonRepository(db)
        self.staff_repo = StaffRepository(db)

    # =========================================================
    # GET MY SALON
    # =========================================================

    async def get_my_salon(self, owner_id: int):

        salon = await self.salon_repo.get_salon_by_owner(
            owner_id
        )

        if not salon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salon not found.",
            )

        return salon

    # =========================================================
    # CREATE STAFF
    # =========================================================

    async def create_staff(
        self,
        salon_id: int,
        owner_id: int,
        data: StaffCreate,
    ):

        salon = await self.get_my_salon(owner_id)

        # Make sure the requested salon belongs
        # to the logged-in salon owner.
        if salon.id != salon_id:
            raise PermissionError(
                "You do not have permission to manage staff for this salon."
            )

        staff = Staff(
            salon_id=salon_id,
            **data.model_dump(),
        )

        return await self.staff_repo.create_staff(staff)

    # =========================================================
    # GET ALL STAFF BY SALON
    # PUBLIC
    # =========================================================

    async def get_staff_by_salon(
        self,
        salon_id: int,
    ):

        return await self.staff_repo.get_all_staff(
            salon_id
        )

    # =========================================================
    # GET SINGLE STAFF
    # PUBLIC
    # =========================================================

    async def get_staff(
        self,
        salon_id: int,
        staff_id: int,
    ):

        return await self.staff_repo.get_staff(
            staff_id,
            salon_id,
        )

    # =========================================================
    # UPDATE STAFF
    # =========================================================

    async def update_staff(
        self,
        salon_id: int,
        staff_id: int,
        owner_id: int,
        data: StaffUpdate,
    ):

        salon = await self.get_my_salon(owner_id)

        # Check ownership
        if salon.id != salon_id:
            raise PermissionError(
                "You do not have permission to update this staff member."
            )

        staff = await self.staff_repo.get_staff(
            staff_id,
            salon_id,
        )

        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found.",
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(staff, field, value)

        return await self.staff_repo.update_staff(
            staff
        )

    # =========================================================
    # DELETE STAFF
    # =========================================================

    async def delete_staff(
        self,
        salon_id: int,
        staff_id: int,
        owner_id: int,
    ):

        salon = await self.get_my_salon(owner_id)

        # Check ownership
        if salon.id != salon_id:
            raise PermissionError(
                "You do not have permission to delete this staff member."
            )

        staff = await self.staff_repo.get_staff(
            staff_id,
            salon_id,
        )

        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found.",
            )

        await self.staff_repo.delete_staff(staff)

        return True