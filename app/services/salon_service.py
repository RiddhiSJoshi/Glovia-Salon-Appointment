from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon_model import (
    Salon,
    Category
)
from app.repositories.salon_repo import SalonRepository
from app.schemas.salon_schema import (
    SalonCreate,
    SalonUpdate,
    CategoryCreate,
    CategoryUpdate
)


class SalonService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = SalonRepository(db)

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


