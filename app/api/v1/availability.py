from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.user_model import User
from app.schemas.availability_schema import (
    WorkingHourCreate,
    WorkingHourResponse,
    StaffLeaveCreate,
    StaffLeaveResponse
)

from app.schemas.staff_schema import (
    StaffCreate,
    StaffResponse,
    StaffUpdate,
)
from app.services.availability_service import AvailabilityService
from app.core.security import get_current_user
from app.dependencies import get_salon_owner


router = APIRouter(
    tags=["Salon Availability"],
)

# =====================================================
# WORKING HOURS
# =====================================================

@router.post(
    "/{salon_id}/working-hours",
    response_model=WorkingHourResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_working_hour(
    data: WorkingHourCreate,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = AvailabilityService(db)

    return await service.create_working_hour(
        current_user.id,
        data,
    )


@router.get(
    "/{salon_id}/working-hours",
    response_model=list[WorkingHourResponse],
)
async def get_working_hours(
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = AvailabilityService(db)

    return await service.get_working_hours(
        current_user.id
    )



# =====================================================
# STAFF LEAVE
# =====================================================

@router.post(
    "/{salon_id}/staff/{staff_id}/leave",
    response_model=StaffLeaveResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_staff_leave(
    staff_id: int,
    data: StaffLeaveCreate,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = AvailabilityService(db)

    return await service.create_staff_leave(
        current_user.id,
        staff_id,
        data,
    )


@router.get(
    "/{salon_id}/staff/{staff_id}/leave",
    response_model=list[StaffLeaveResponse],
)
async def get_staff_leave(
    staff_id: int,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = AvailabilityService(db)

    return await service.get_staff_leaves(
        current_user.id,
        staff_id,
    )
@router.post(
    "/{salon_id}/staff",
    response_model=StaffResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_staff(
    data: StaffCreate,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = AvailabilityService(db)

    return await service.create_staff(
        current_user.id,
        data,
    )


@router.get(
    "/{salon_id}/staff",
    response_model=list[StaffResponse],
)
async def get_staff(
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = AvailabilityService(db)

    return await service.get_staff(
        current_user.id
    )


@router.put(
    "/{salon_id}/staff/{staff_id}",
    response_model=StaffResponse,
)
async def update_staff(
    staff_id: int,
    data: StaffUpdate,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = AvailabilityService(db)

    return await service.update_staff(
        current_user.id,
        staff_id,
        data,
    )


@router.delete(
    "/{salon_id}/staff/{staff_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_staff(
    staff_id: int,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = AvailabilityService(db)

    await service.delete_staff(
        current_user.id,
        staff_id,
    )
