from datetime import datetime, timedelta

from app.models.salon_model import (
    Appointment,
    AppointmentStatus,
)

from app.repositories.appointment_repo import (
    AppointmentRepository,
)

from app.schemas.appointment_schema import (
    AppointmentCreate,
    AppointmentReschedule,
)


class AppointmentService:

    def __init__(self, db):
        self.db = db
        self.repo = AppointmentRepository(db)

    # ============================================================
    # CREATE APPOINTMENT
    # ============================================================

    async def create_appointment(
        self,
        customer_id: int,
        data: AppointmentCreate,
    ):

        # --------------------------------------------------------
        # Get salon
        # --------------------------------------------------------

        salon = await self.repo.get_salon(
            data.salon_id
        )

        if not salon:
            raise ValueError(
                "Salon not found."
            )

        if not salon.is_active:
            raise ValueError(
                "Salon is currently inactive."
            )

        # --------------------------------------------------------
        # Get service
        # --------------------------------------------------------

        service = await self.repo.get_service(
            data.service_id
        )

        if not service:
            raise ValueError(
                "Service not found."
            )

        if not service.is_active:
            raise ValueError(
                "Service is currently unavailable."
            )

        # Service must belong to selected salon
        if service.salon_id != data.salon_id:
            raise ValueError(
                "Service does not belong to this salon."
            )

        # --------------------------------------------------------
        # Get staff
        # --------------------------------------------------------

        staff = await self.repo.get_staff(
            data.staff_id
        )

        if not staff:
            raise ValueError(
                "Staff member not found."
            )

        if not staff.is_active:
            raise ValueError(
                "Selected staff member is inactive."
            )

        # Staff must belong to selected salon
        if staff.salon_id != data.salon_id:
            raise ValueError(
                "Staff member does not belong to this salon."
            )

        # --------------------------------------------------------
        # Calculate appointment end time
        # --------------------------------------------------------

        start_time = data.start_time

        end_time = (
            start_time
            + timedelta(
                minutes=service.duration_minutes
            )
        )

        # --------------------------------------------------------
        # Check working hours
        # --------------------------------------------------------

        # Python weekday:
        # Monday = 0
        # Sunday = 6

        day_of_week = start_time.weekday()

        working_hour = await self.repo.get_working_hour(
            salon_id=data.salon_id,
            day_of_week=day_of_week,
        )

        if not working_hour:
            raise ValueError(
                "Working hours are not configured for this day."
            )

        if working_hour.is_closed:
            raise ValueError(
                "Salon is closed on the selected day."
            )

        start_time_only = start_time.time()
        end_time_only = end_time.time()

        if (
            start_time_only < working_hour.opening_time
            or end_time_only > working_hour.closing_time
        ):
            raise ValueError(
                "Appointment is outside salon working hours."
            )

        # --------------------------------------------------------
        # Check staff leave
        # --------------------------------------------------------

        staff_leave = await self.repo.get_staff_leave(
            staff_id=data.staff_id,
            start_time=start_time.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            ),
            end_time=(
                start_time.replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                )
                + timedelta(days=1)
            ),
        )

        if staff_leave:
            raise ValueError(
                "Selected staff member is on leave."
            )

        # --------------------------------------------------------
        # Check appointment conflict
        # --------------------------------------------------------

        conflict = await self.repo.get_conflicting_appointment(
            staff_id=data.staff_id,
            start_time=start_time,
            end_time=end_time,
        )

        if conflict:
            raise ValueError(
                "Selected time slot is no longer available."
            )

        # --------------------------------------------------------
        # Create appointment
        # --------------------------------------------------------

        appointment = Appointment(
            customer_id=customer_id,
            salon_id=data.salon_id,
            staff_id=data.staff_id,
            service_id=data.service_id,
            start_time=start_time,
            end_time=end_time,
            status=AppointmentStatus.PENDING,
        )

        return await self.repo.create(
            appointment
        )

    # ============================================================
    # CUSTOMER APPOINTMENTS
    # ============================================================

    async def get_customer_appointments(
        self,
        customer_id: int,
    ):

        return await self.repo.get_customer_appointments(
            customer_id
        )

    # ============================================================
    # GET APPOINTMENT
    # ============================================================

    async def get_appointment(
        self,
        appointment_id: int,
        user_id: int,
    ):

        appointment = await self.repo.get_by_id(
            appointment_id
        )

        if not appointment:
            return None

        # Customer can only see their own appointment
        if appointment.customer_id != user_id:
            raise PermissionError()

        return appointment

    # ============================================================
    # CANCEL APPOINTMENT
    # ============================================================

    async def cancel_appointment(
        self,
        appointment_id: int,
        user_id: int,
    ):

        appointment = await self.repo.get_by_id(
            appointment_id
        )

        if not appointment:
            return None

        if appointment.customer_id != user_id:
            raise PermissionError()

        if appointment.status in [
            AppointmentStatus.CANCELLED,
            AppointmentStatus.COMPLETED,
        ]:
            raise ValueError(
                "This appointment cannot be cancelled."
            )

        appointment.status = AppointmentStatus.CANCELLED

        return await self.repo.update(
            appointment
        )

    # ============================================================
    # RESCHEDULE
    # ============================================================

    async def reschedule_appointment(
        self,
        appointment_id: int,
        user_id: int,
        data: AppointmentReschedule,
    ):

        appointment = await self.repo.get_by_id(
            appointment_id
        )

        if not appointment:
            return None

        if appointment.customer_id != user_id:
            raise PermissionError()

        if appointment.status in [
            AppointmentStatus.CANCELLED,
            AppointmentStatus.COMPLETED,
        ]:
            raise ValueError(
                "This appointment cannot be rescheduled."
            )

        # Get service
        service = await self.repo.get_service(
            appointment.service_id
        )

        if not service:
            raise ValueError(
                "Service not found."
            )

        new_start = data.start_time

        new_end = (
            new_start
            + timedelta(
                minutes=service.duration_minutes
            )
        )

        # --------------------------------------------------------
        # Working hours
        # --------------------------------------------------------

        day_of_week = new_start.weekday()

        working_hour = await self.repo.get_working_hour(
            salon_id=appointment.salon_id,
            day_of_week=day_of_week,
        )

        if not working_hour:
            raise ValueError(
                "Working hours are not configured for this day."
            )

        if working_hour.is_closed:
            raise ValueError(
                "Salon is closed on the selected day."
            )

        if (
            new_start.time() < working_hour.opening_time
            or new_end.time() > working_hour.closing_time
        ):
            raise ValueError(
                "Appointment is outside salon working hours."
            )

        # --------------------------------------------------------
        # Staff leave
        # --------------------------------------------------------

        day_start = new_start.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        day_end = day_start + timedelta(days=1)

        staff_leave = await self.repo.get_staff_leave(
            staff_id=appointment.staff_id,
            start_time=day_start,
            end_time=day_end,
        )

        if staff_leave:
            raise ValueError(
                "Selected staff member is on leave."
            )

        # --------------------------------------------------------
        # Conflict
        # --------------------------------------------------------

        conflict = await self.repo.get_conflicting_appointment(
            staff_id=appointment.staff_id,
            start_time=new_start,
            end_time=new_end,
            exclude_appointment_id=appointment.id,
        )

        if conflict:
            raise ValueError(
                "Selected time slot is no longer available."
            )

        appointment.start_time = new_start
        appointment.end_time = new_end

        return await self.repo.update(
            appointment
        )

    # ============================================================
    # SALON APPOINTMENTS
    # ============================================================

    async def get_salon_appointments(
        self,
        salon_id: int,
        owner_id: int,
    ):

        salon = await self.repo.get_salon(
            salon_id
        )

        if not salon:
            raise ValueError(
                "Salon not found."
            )

        if salon.owner_id != owner_id:
            raise PermissionError()

        return await self.repo.get_salon_appointments(
            salon_id
        )

    # ============================================================
    # CONFIRM
    # ============================================================

    async def confirm_appointment(
        self,
        salon_id: int,
        appointment_id: int,
        owner_id: int,
    ):

        appointment = await self.repo.get_by_id(
            appointment_id
        )

        if not appointment:
            return None

        await self._verify_salon_owner(
            salon_id,
            owner_id,
            appointment,
        )

        if appointment.status != AppointmentStatus.PENDING:
            raise ValueError(
                "Only pending appointments can be confirmed."
            )

        appointment.status = AppointmentStatus.CONFIRMED

        return await self.repo.update(
            appointment
        )

    # ============================================================
    # REJECT
    # ============================================================

    async def reject_appointment(
        self,
        salon_id: int,
        appointment_id: int,
        owner_id: int,
    ):

        appointment = await self.repo.get_by_id(
            appointment_id
        )

        if not appointment:
            return None

        await self._verify_salon_owner(
            salon_id,
            owner_id,
            appointment,
        )

        if appointment.status != AppointmentStatus.PENDING:
            raise ValueError(
                "Only pending appointments can be rejected."
            )

        appointment.status = AppointmentStatus.CANCELLED

        return await self.repo.update(
            appointment
        )

    # ============================================================
    # COMPLETE
    # ============================================================

    async def complete_appointment(
        self,
        salon_id: int,
        appointment_id: int,
        owner_id: int,
    ):

        appointment = await self.repo.get_by_id(
            appointment_id
        )

        if not appointment:
            return None

        await self._verify_salon_owner(
            salon_id,
            owner_id,
            appointment,
        )

        if appointment.status != AppointmentStatus.CONFIRMED:
            raise ValueError(
                "Only confirmed appointments can be completed."
            )

        appointment.status = AppointmentStatus.COMPLETED

        return await self.repo.update(
            appointment
        )

    # ============================================================
    # OWNER VALIDATION
    # ============================================================

    async def _verify_salon_owner(
        self,
        salon_id: int,
        owner_id: int,
        appointment: Appointment,
    ):

        if appointment.salon_id != salon_id:
            raise PermissionError()

        salon = await self.repo.get_salon(
            salon_id
        )

        if not salon:
            raise ValueError(
                "Salon not found."
            )

        if salon.owner_id != owner_id:
            raise PermissionError()