from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon_model import (
    Staff
)
from app.repositories.salon_repo import SalonRepository
from app.schemas.staff_schema import (
    StaffCreate,
    StaffUpdate
)

class StaffService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = SalonRepository(db)
    # =========================
    # STAFF
    # =========================

    async def create_staff(
        self,
        owner_id: int,
        data: StaffCreate,
    ):

        salon = await self.get_my_salon(owner_id)

        staff = Staff(
            salon_id=salon.id,
            **data.model_dump(),
        )

        return await self.repo.create_staff(staff)

    async def get_staff(self, owner_id: int):

        salon = await self.get_my_salon(owner_id)

        return await self.repo.get_all_staff(salon.id)

    async def update_staff(
        self,
        owner_id: int,
        staff_id: int,
        data: StaffUpdate,
    ):

        salon = await self.get_my_salon(owner_id)

        staff = await self.repo.get_staff(
            staff_id,
            salon.id,
        )

        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found",
            )

        for field, value in data.model_dump(
            exclude_unset=True
        ).items():
            setattr(staff, field, value)

        return await self.repo.update_staff(staff)

    async def delete_staff(
        self,
        owner_id: int,
        staff_id: int,
    ):

        salon = await self.get_my_salon(owner_id)

        staff = await self.repo.get_staff(
            staff_id,
            salon.id,
        )

        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found",
            )

        await self.repo.delete_staff(staff)