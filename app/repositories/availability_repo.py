from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon_model import (
    WorkingHour,
    StaffLeave,
)


class AvailabilityRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    # =========================================================
    # WORKING HOURS
    # =========================================================

    async def create_working_hour(
        self,
        working_hour: WorkingHour,
    ):
        self.db.add(working_hour)

        await self.db.commit()
        await self.db.refresh(working_hour)

        return working_hour

    async def get_working_hours(
        self,
        salon_id: int,
    ):
        result = await self.db.execute(
            select(WorkingHour)
            .where(
                WorkingHour.salon_id == salon_id
            )
            .order_by(
                WorkingHour.day_of_week
            )
        )

        return result.scalars().all()

    # =========================================================
    # STAFF LEAVE
    # =========================================================

    async def create_leave(
        self,
        leave: StaffLeave,
    ):
        self.db.add(leave)

        await self.db.commit()
        await self.db.refresh(leave)

        return leave

    async def get_leaves(
        self,
        staff_id: int,
    ):
        result = await self.db.execute(
            select(StaffLeave)
            .where(
                StaffLeave.staff_id == staff_id
            )
            .order_by(
                StaffLeave.leave_date
            )
        )

        return result.scalars().all()