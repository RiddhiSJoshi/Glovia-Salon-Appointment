from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon_model import (
    Salon,
    Category,
    Service,
    Staff,
    WorkingHour,
    StaffLeave,
    Appointment,
)


class SalonRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    # =========================
    # SALON
    # =========================

    async def create_salon(self, salon: Salon):
        self.db.add(salon)
        await self.db.commit()
        await self.db.refresh(salon)
        return salon

    async def get_salon(self, salon_id: int):
        result = await self.db.execute(
            select(Salon).where(Salon.id == salon_id)
        )
        return result.scalar_one_or_none()

    async def get_salon_by_owner(self, owner_id: int):
        result = await self.db.execute(
            select(Salon).where(Salon.owner_id == owner_id)
        )
        return result.scalar_one_or_none()

    async def update_salon(self, salon: Salon):
        await self.db.commit()
        await self.db.refresh(salon)
        return salon

    async def delete_salon(self, salon: Salon):
        await self.db.delete(salon)
        await self.db.commit()

    # =========================
    # CATEGORY
    # =========================

    async def create_category(self, category: Category):
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def get_category(
        self,
        category_id: int,
        salon_id: int,
    ):
        result = await self.db.execute(
            select(Category).where(
                Category.id == category_id,
                Category.salon_id == salon_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_categories(self, salon_id: int):
        result = await self.db.execute(
            select(Category)
            .where(Category.salon_id == salon_id)
            .order_by(Category.name)
        )
        return result.scalars().all()

    async def update_category(self, category: Category):
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete_category(self, category: Category):
        await self.db.delete(category)
        await self.db.commit()

    
    
