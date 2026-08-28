from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon import (
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

    # =========================
    # SERVICE
    # =========================

    async def create_service(self, service: Service):
        self.db.add(service)
        await self.db.commit()
        await self.db.refresh(service)
        return service

    async def get_service(
        self,
        service_id: int,
        salon_id: int,
    ):
        result = await self.db.execute(
            select(Service).where(
                Service.id == service_id,
                Service.salon_id == salon_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_services(self, salon_id: int):
        result = await self.db.execute(
            select(Service)
            .where(Service.salon_id == salon_id)
            .order_by(Service.name)
        )
        return result.scalars().all()

    async def update_service(self, service: Service):
        await self.db.commit()
        await self.db.refresh(service)
        return service

    async def delete_service(self, service: Service):
        await self.db.delete(service)
        await self.db.commit()

    # =========================
    # STAFF
    # =========================

    async def create_staff(self, staff: Staff):
        self.db.add(staff)
        await self.db.commit()
        await self.db.refresh(staff)
        return staff

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

    async def get_all_staff(self, salon_id: int):
        result = await self.db.execute(
            select(Staff)
            .where(Staff.salon_id == salon_id)
            .order_by(Staff.name)
        )
        return result.scalars().all()

    async def update_staff(self, staff: Staff):
        await self.db.commit()
        await self.db.refresh(staff)
        return staff

    async def delete_staff(self, staff: Staff):
        await self.db.delete(staff)
        await self.db.commit()

    # =========================
    # WORKING HOURS
    # =========================

    async def create_working_hour(
        self,
        working_hour: WorkingHour,
    ):
        self.db.add(working_hour)
        await self.db.commit()
        await self.db.refresh(working_hour)
        return working_hour

    async def get_working_hours(self, salon_id: int):
        result = await self.db.execute(
            select(WorkingHour)
            .where(WorkingHour.salon_id == salon_id)
            .order_by(WorkingHour.day_of_week)
        )
        return result.scalars().all()

    # =========================
    # LEAVE
    # =========================

    async def create_leave(self, leave: StaffLeave):
        self.db.add(leave)
        await self.db.commit()
        await self.db.refresh(leave)
        return leave

    async def get_leaves(self, staff_id: int):
        result = await self.db.execute(
            select(StaffLeave)
            .where(StaffLeave.staff_id == staff_id)
            .order_by(StaffLeave.leave_date)
        )
        return result.scalars().all()

    # =========================
    # APPOINTMENTS
    # =========================

    async def get_appointments(self, salon_id: int):
        result = await self.db.execute(
            select(Appointment)
            .where(Appointment.salon_id == salon_id)
            .order_by(Appointment.start_time)
        )
        return result.scalars().all()