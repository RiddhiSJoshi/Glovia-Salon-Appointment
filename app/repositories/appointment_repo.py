from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon_model import (
    Appointment,
    AppointmentStatus,
    Salon,
    Service,
    Staff,
    StaffLeave,
    WorkingHour,
)


class AppointmentRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    # ============================================================
    # APPOINTMENT
    # ============================================================

    async def get_by_id(
        self,
        appointment_id: int,
    ) -> Appointment | None:

        result = await self.db.execute(
            select(Appointment).where(
                Appointment.id == appointment_id
            )
        )

        return result.scalar_one_or_none()

    async def get_customer_appointments(
        self,
        customer_id: int,
    ) -> list[Appointment]:

        result = await self.db.execute(
            select(Appointment)
            .where(
                Appointment.customer_id == customer_id
            )
            .order_by(Appointment.start_time.desc())
        )

        return list(result.scalars().all())

    async def get_salon_appointments(
        self,
        salon_id: int,
    ) -> list[Appointment]:

        result = await self.db.execute(
            select(Appointment)
            .where(
                Appointment.salon_id == salon_id
            )
            .order_by(Appointment.start_time.asc())
        )

        return list(result.scalars().all())

    async def create(
        self,
        appointment: Appointment,
    ) -> Appointment:

        self.db.add(appointment)

        await self.db.commit()
        await self.db.refresh(appointment)

        return appointment

    async def update(
        self,
        appointment: Appointment,
    ) -> Appointment:

        await self.db.commit()
        await self.db.refresh(appointment)

        return appointment

    # ============================================================
    # SALON
    # ============================================================

    async def get_salon(
        self,
        salon_id: int,
    ) -> Salon | None:

        result = await self.db.execute(
            select(Salon).where(
                Salon.id == salon_id
            )
        )

        return result.scalar_one_or_none()

    # ============================================================
    # SERVICE
    # ============================================================

    async def get_service(
        self,
        service_id: int,
    ) -> Service | None:

        result = await self.db.execute(
            select(Service).where(
                Service.id == service_id
            )
        )

        return result.scalar_one_or_none()

    # ============================================================
    # STAFF
    # ============================================================

    async def get_staff(
        self,
        staff_id: int,
    ) -> Staff | None:

        result = await self.db.execute(
            select(Staff).where(
                Staff.id == staff_id
            )
        )

        return result.scalar_one_or_none()

    # ============================================================
    # WORKING HOURS
    # ============================================================

    async def get_working_hour(
        self,
        salon_id: int,
        day_of_week: int,
    ) -> WorkingHour | None:

        result = await self.db.execute(
            select(WorkingHour).where(
                WorkingHour.salon_id == salon_id,
                WorkingHour.day_of_week == day_of_week,
            )
        )

        return result.scalar_one_or_none()

    # ============================================================
    # STAFF LEAVE
    # ============================================================

    async def get_staff_leave(
        self,
        staff_id: int,
        start_time: datetime,
        end_time: datetime,
    ) -> StaffLeave | None:

        result = await self.db.execute(
            select(StaffLeave).where(
                StaffLeave.staff_id == staff_id,
                StaffLeave.leave_date >= start_time,
                StaffLeave.leave_date < end_time,
            )
        )

        return result.scalar_one_or_none()

    # ============================================================
    # AVAILABILITY
    # ============================================================

    async def get_conflicting_appointment(
        self,
        staff_id: int,
        start_time: datetime,
        end_time: datetime,
        exclude_appointment_id: int | None = None,
    ) -> Appointment | None:

        query = select(Appointment).where(
            Appointment.staff_id == staff_id,

            Appointment.status.in_(
                [
                    AppointmentStatus.PENDING,
                    AppointmentStatus.CONFIRMED,
                ]
            ),

            Appointment.start_time < end_time,
            Appointment.end_time > start_time,
        )

        if exclude_appointment_id is not None:
            query = query.where(
                Appointment.id != exclude_appointment_id
            )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()