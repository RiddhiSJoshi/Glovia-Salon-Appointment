from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon_model import (
    WorkingHour,
    StaffLeave,
)

from app.repositories.salon_repo import SalonRepository
from app.repositories.availability_repo import AvailabilityRepository
from app.repositories.staff_repo import StaffRepository

from app.schemas.availability_schema import (
    WorkingHourCreate,
    StaffLeaveCreate,
)


class AvailabilityService:

    def __init__(self, db: AsyncSession):
        self.db = db

        self.salon_repo = SalonRepository(db)
        self.availability_repo = AvailabilityRepository(db)
        self.staff_repo = StaffRepository(db)

    # =========================================================
    # GET MY SALON
    # =========================================================

    async def get_my_salon(
        self,
        owner_id: int,
    ):

        salon = await self.salon_repo.get_salon_by_owner(
            owner_id
        )

        if not salon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salon not found for this owner.",
            )

        return salon

    # =========================================================
    # WORKING HOURS
    # =========================================================

    async def create_working_hour(
        self,
        owner_id: int,
        data: WorkingHourCreate,
    ):

        salon = await self.get_my_salon(
            owner_id
        )

        working_hour = WorkingHour(
            salon_id=salon.id,
            **data.model_dump(),
        )

        return await self.availability_repo.create_working_hour(
            working_hour
        )

    async def get_working_hours(
        self,
        owner_id: int,
    ):

        salon = await self.get_my_salon(
            owner_id
        )

        return await self.availability_repo.get_working_hours(
            salon.id
        )

    # =========================================================
    # STAFF LEAVE
    # =========================================================

    async def create_staff_leave(
        self,
        owner_id: int,
        staff_id: int,
        data: StaffLeaveCreate,
    ):

        salon = await self.get_my_salon(
            owner_id
        )

        staff = await self.staff_repo.get_staff(
            staff_id=staff_id,
            salon_id=salon.id,
        )

        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found.",
            )

        leave = StaffLeave(
            staff_id=staff.id,
            **data.model_dump(),
        )

        return await self.availability_repo.create_leave(
            leave
        )

    async def get_staff_leaves(
        self,
        owner_id: int,
        staff_id: int,
    ):

        salon = await self.get_my_salon(
            owner_id
        )

        staff = await self.staff_repo.get_staff(
            staff_id=staff_id,
            salon_id=salon.id,
        )

        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found.",
            )

        return await self.availability_repo.get_leaves(
            staff_id
        )