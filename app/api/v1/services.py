
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.user_model import User
from app.schemas.service_schema import (
    ServiceCreate,
    ServiceUpdate,
    ServiceResponse,
)
from app.services.service_service import ServicesService
from app.dependencies import get_salon_owner


router = APIRouter(
    tags=["Salon Service"],
)


# ============================================================
# CREATE SERVICE
# ============================================================

@router.post(
    "/{salon_id}/services",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_service(
    data: ServiceCreate,
    salon_id: int = Path(..., gt=0),
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = ServicesService(db)

    return await service.create_service(
        salon_id=salon_id,
        owner_id=current_user.id,
        data=data,
    )


# ============================================================
# GET ALL SERVICES
# ============================================================

@router.get(
    "/{salon_id}/services",
    response_model=list[ServiceResponse],
    status_code=status.HTTP_200_OK,
)
async def get_services(
    salon_id: int = Path(..., gt=0),
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = ServicesService(db)

    return await service.get_services(
        salon_id=salon_id,
        owner_id=current_user.id,
    )


# ============================================================
# UPDATE SERVICE
# ============================================================

@router.put(
    "/{salon_id}/services/{service_id}",
    response_model=ServiceResponse,
    status_code=status.HTTP_200_OK,
)
async def update_service(
    data: ServiceUpdate,
    salon_id: int = Path(..., gt=0),
    service_id: int = Path(..., gt=0),
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = ServicesService(db)

    return await service.update_service(
        salon_id=salon_id,
        service_id=service_id,
        owner_id=current_user.id,
        data=data,
    )


# ============================================================
# DELETE SERVICE
# ============================================================

@router.delete(
    "/{salon_id}/services/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_service(
    salon_id: int = Path(..., gt=0),
    service_id: int = Path(..., gt=0),
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = ServicesService(db)

    await service.delete_service(
        salon_id=salon_id,
        service_id=service_id,
        owner_id=current_user.id,
    )

    return None

