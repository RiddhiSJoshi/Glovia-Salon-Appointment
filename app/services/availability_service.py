from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon_model import (
    Salon,
    Category,
    WorkingHour,
    StaffLeave,
)
from app.repositories.salon_repo import SalonRepository
from app.schemas.availability_schema import (
    WorkingHourCreate,
    StaffLeaveCreate,
)


class AvailabilityService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = SalonRepository(db)

    async def create_working_hour(
        self,
        owner_id: int,
        data: WorkingHourCreate,
    ):

        salon = await self.get_my_salon(owner_id)

        working_hour = WorkingHour(
            salon_id=salon.id,
            **data.model_dump(),
        )

        return await self.repo.create_working_hour(
            working_hour
        )

    async def get_working_hours(
        self,
        owner_id: int,
    ):

        salon = await self.get_my_salon(owner_id)

        return await self.repo.get_working_hours(
            salon.id
        )


    async def create_staff_leave(
        self,
        owner_id: int,
        staff_id: int,
        data: StaffLeaveCreate,
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

        leave = StaffLeave(
            staff_id=staff.id,
            **data.model_dump(),
        )

        return await self.repo.create_leave(leave)

    async def get_staff_leaves(
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

        return await self.repo.get_leaves(staff_id)