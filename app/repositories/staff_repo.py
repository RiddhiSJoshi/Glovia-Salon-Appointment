from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon_model import Staff


class StaffRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    # =========================================================
    # CREATE
    # =========================================================

    async def create_staff(
        self,
        staff: Staff,
    ):
        self.db.add(staff)

        await self.db.commit()
        await self.db.refresh(staff)

        return staff

    # =========================================================
    # GET SINGLE STAFF
    # =========================================================

    async def get_staff(
        self,
        staff_id: int,
        salon_id: int,
    ):
        result = await self.db.execute(
            select(Staff).where(
                Staff.id == staff_id,
                Staff.salon_id == salon_id,
            )
        )

        return result.scalar_one_or_none()

    # =========================================================
    # GET ALL STAFF
    # =========================================================

    async def get_all_staff(
        self,
        salon_id: int,
    ):
        result = await self.db.execute(
            select(Staff)
            .where(
                Staff.salon_id == salon_id
            )
            .order_by(Staff.name)
        )

        return result.scalars().all()

    # =========================================================
    # UPDATE
    # =========================================================

    async def update_staff(
        self,
        staff: Staff,
    ):
        await self.db.commit()
        await self.db.refresh(staff)

        return staff

    # =========================================================
    # DELETE
    # =========================================================

    async def delete_staff(
        self,
        staff: Staff,
    ):
        await self.db.delete(staff)
        await self.db.commit()