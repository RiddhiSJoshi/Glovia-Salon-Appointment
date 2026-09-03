from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon_model import (
    Service
)


class ServiceRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    
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