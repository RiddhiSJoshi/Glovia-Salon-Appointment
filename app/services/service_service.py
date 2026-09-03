from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon_model import (
    Service
)
from app.repositories.salon_repo import SalonRepository
from app.schemas.service_schema import (
    ServiceCreate,
    ServiceUpdate
)

class ServicesService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = SalonRepository(db)
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
