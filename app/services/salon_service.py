from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon import (
    Salon,
    Category,
    Service,
    Staff,
    WorkingHour,
    StaffLeave,
)
from app.repositories.salon_repo import SalonRepository
from app.schemas.salon import (
    SalonCreate,
    SalonUpdate,
    CategoryCreate,
    CategoryUpdate,
    ServiceCreate,
    ServiceUpdate,
    StaffCreate,
    StaffUpdate,
    WorkingHourCreate,
    StaffLeaveCreate,
)


class SalonService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = SalonRepository(db)

    # =========================
    # SALON
    # =========================

    async def create_salon(
        self,
        owner_id: int,
        data: SalonCreate,
    ):

        existing = await self.repo.get_salon_by_owner(owner_id)

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Salon already exists for this owner",
            )

        salon = Salon(
            owner_id=owner_id,
            **data.model_dump(),
        )

        return await self.repo.create_salon(salon)

    async def get_my_salon(self, owner_id: int):

        salon = await self.repo.get_salon_by_owner(owner_id)

        if not salon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salon not found",
            )

        return salon

    async def update_salon(
        self,
        owner_id: int,
        data: SalonUpdate,
    ):

        salon = await self.get_my_salon(owner_id)

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(salon, field, value)

        return await self.repo.update_salon(salon)

    async def delete_salon(self, owner_id: int):

        salon = await self.get_my_salon(owner_id)

        await self.repo.delete_salon(salon)

    # =========================
    # CATEGORY
    # =========================

    async def create_category(
        self,
        owner_id: int,
        data: CategoryCreate,
    ):

        salon = await self.get_my_salon(owner_id)

        category = Category(
            salon_id=salon.id,
            **data.model_dump(),
        )

        return await self.repo.create_category(category)

    async def get_categories(self, owner_id: int):

        salon = await self.get_my_salon(owner_id)

        return await self.repo.get_categories(salon.id)

    async def update_category(
        self,
        owner_id: int,
        category_id: int,
        data: CategoryUpdate,
    ):

        salon = await self.get_my_salon(owner_id)

        category = await self.repo.get_category(
            category_id,
            salon.id,
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        for field, value in data.model_dump(
            exclude_unset=True
        ).items():
            setattr(category, field, value)

        return await self.repo.update_category(category)

    async def delete_category(
        self,
        owner_id: int,
        category_id: int,
    ):

        salon = await self.get_my_salon(owner_id)

        category = await self.repo.get_category(
            category_id,
            salon.id,
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        await self.repo.delete_category(category)

    # =========================
    # SERVICES
    # =========================

    async def create_service(
        self,
        owner_id: int,
        data: ServiceCreate,
    ):

        salon = await self.get_my_salon(owner_id)

        if data.category_id:

            category = await self.repo.get_category(
                data.category_id,
                salon.id,
            )

            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category does not belong to this salon",
                )

        service = Service(
            salon_id=salon.id,
            **data.model_dump(),
        )

        return await self.repo.create_service(service)

    async def get_services(self, owner_id: int):

        salon = await self.get_my_salon(owner_id)

        return await self.repo.get_services(salon.id)

    async def update_service(
        self,
        owner_id: int,
        service_id: int,
        data: ServiceUpdate,
    ):

        salon = await self.get_my_salon(owner_id)

        service = await self.repo.get_service(
            service_id,
            salon.id,
        )

        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found",
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "category_id" in update_data:
            category_id = update_data["category_id"]

            if category_id:

                category = await self.repo.get_category(
                    category_id,
                    salon.id,
                )

                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Category does not belong to this salon",
                    )

        for field, value in update_data.items():
            setattr(service, field, value)

        return await self.repo.update_service(service)

    async def delete_service(
        self,
        owner_id: int,
        service_id: int,
    ):

        salon = await self.get_my_salon(owner_id)

        service = await self.repo.get_service(
            service_id,
            salon.id,
        )

        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found",
            )

        await self.repo.delete_service(service)

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

    # =========================
    # WORKING HOURS
    # =========================

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

    # =========================
    # STAFF LEAVE
    # =========================

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