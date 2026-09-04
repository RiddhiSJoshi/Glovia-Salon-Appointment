from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon_model import Service
from app.repositories.salon_repo import SalonRepository
from app.repositories.service_repo import ServiceRepository
from app.schemas.service_schema import (
    ServiceCreate,
    ServiceUpdate,
)


class ServicesService:

    def __init__(self, db: AsyncSession):
        self.db = db

        # Salon/category operations
        self.salon_repo = SalonRepository(db)

        # Service operations
        self.service_repo = ServiceRepository(db)

    # ========================================================
    # GET MY SALON
    # ========================================================

    async def get_my_salon(self, owner_id: int):

        salon = await self.salon_repo.get_salon_by_owner(
            owner_id
        )

        if not salon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salon not found",
            )

        return salon

    # ========================================================
    # CREATE SERVICE
    # ========================================================

    async def create_service(
        self,
        owner_id: int,
        data: ServiceCreate,
    ):

        salon = await self.get_my_salon(owner_id)

        # Validate category belongs to this salon
        if data.category_id:

            category = await self.salon_repo.get_category(
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

        return await self.service_repo.create_service(
            service
        )

    # ========================================================
    # GET ALL SERVICES
    # ========================================================

    async def get_services(
        self,
        owner_id: int,
    ):

        salon = await self.get_my_salon(owner_id)

        return await self.service_repo.get_services(
            salon.id
        )

    # ========================================================
    # UPDATE SERVICE
    # ========================================================

    async def update_service(
        self,
        owner_id: int,
        service_id: int,
        data: ServiceUpdate,
    ):

        salon = await self.get_my_salon(owner_id)

        # Make sure the service belongs to this owner's salon
        service = await self.service_repo.get_service(
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

        # Validate category if it is being changed
        if "category_id" in update_data:

            category_id = update_data["category_id"]

            if category_id:

                category = await self.salon_repo.get_category(
                    category_id,
                    salon.id,
                )

                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Category does not belong to this salon",
                    )

        # Apply updates
        for field, value in update_data.items():
            setattr(service, field, value)

        return await self.service_repo.update_service(
            service
        )

    # ========================================================
    # DELETE SERVICE
    # ========================================================

    async def delete_service(
        self,
        owner_id: int,
        service_id: int,
    ):

        salon = await self.get_my_salon(owner_id)

        # Make sure the service belongs to this owner's salon
        service = await self.service_repo.get_service(
            service_id,
            salon.id,
        )

        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found",
            )

        await self.service_repo.delete_service(
            service
        )