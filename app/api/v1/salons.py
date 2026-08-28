from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.user import User
from app.schemas.salon import (
    SalonCreate,
    SalonUpdate,
    SalonResponse,
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    ServiceCreate,
    ServiceUpdate,
    ServiceResponse,
    StaffCreate,
    StaffUpdate,
    StaffResponse,
    WorkingHourCreate,
    WorkingHourResponse,
    StaffLeaveCreate,
    StaffLeaveResponse,
)
from app.services.salon_service import SalonService
from app.core.security import get_current_user
from app.dependencies import get_salon_owner


router = APIRouter(
    tags=["Salon Management"],
)


# =====================================================
# SALON
# =====================================================

@router.post(
    "/",
    response_model=SalonResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_salon(
    data: SalonCreate,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    return await service.create_salon(
        current_user.id,
        data,
    )


@router.get(
    "/me",
    response_model=SalonResponse,
)
async def get_my_salon(
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    return await service.get_my_salon(
        current_user.id
    )


@router.patch(
    "/me",
    response_model=SalonResponse,
)
async def update_my_salon(
    data: SalonUpdate,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    return await service.update_salon(
        current_user.id,
        data,
    )


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_my_salon(
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    await service.delete_salon(
        current_user.id
    )


# =====================================================
# CATEGORY
# =====================================================

@router.post(
    "/me/categories",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    data: CategoryCreate,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    return await service.create_category(
        current_user.id,
        data,
    )


@router.get(
    "/me/categories",
    response_model=list[CategoryResponse],
)
async def get_categories(
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    return await service.get_categories(
        current_user.id
    )


@router.patch(
    "/me/categories/{category_id}",
    response_model=CategoryResponse,
)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    return await service.update_category(
        current_user.id,
        category_id,
        data,
    )


@router.delete(
    "/me/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    await service.delete_category(
        current_user.id,
        category_id,
    )


# =====================================================
# SERVICES
# =====================================================

@router.post(
    "/me/services",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_service(
    data: ServiceCreate,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    return await service.create_service(
        current_user.id,
        data,
    )


@router.get(
    "/me/services",
    response_model=list[ServiceResponse],
)
async def get_services(
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    return await service.get_services(
        current_user.id
    )


@router.patch(
    "/me/services/{service_id}",
    response_model=ServiceResponse,
)
async def update_service(
    service_id: int,
    data: ServiceUpdate,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    return await service.update_service(
        current_user.id,
        service_id,
        data,
    )


@router.delete(
    "/me/services/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_service(
    service_id: int,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    await service.delete_service(
        current_user.id,
        service_id,
    )


# =====================================================
# STAFF
# =====================================================

@router.post(
    "/me/staff",
    response_model=StaffResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_staff(
    data: StaffCreate,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    return await service.create_staff(
        current_user.id,
        data,
    )


@router.get(
    "/me/staff",
    response_model=list[StaffResponse],
)
async def get_staff(
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    return await service.get_staff(
        current_user.id
    )


@router.patch(
    "/me/staff/{staff_id}",
    response_model=StaffResponse,
)
async def update_staff(
    staff_id: int,
    data: StaffUpdate,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    return await service.update_staff(
        current_user.id,
        staff_id,
        data,
    )


@router.delete(
    "/me/staff/{staff_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_staff(
    staff_id: int,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    await service.delete_staff(
        current_user.id,
        staff_id,
    )


# =====================================================
# WORKING HOURS
# =====================================================

@router.post(
    "/me/working-hours",
    response_model=WorkingHourResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_working_hour(
    data: WorkingHourCreate,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    return await service.create_working_hour(
        current_user.id,
        data,
    )


@router.get(
    "/me/working-hours",
    response_model=list[WorkingHourResponse],
)
async def get_working_hours(
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    return await service.get_working_hours(
        current_user.id
    )


# =====================================================
# STAFF LEAVE
# =====================================================

@router.post(
    "/me/staff/{staff_id}/leave",
    response_model=StaffLeaveResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_staff_leave(
    staff_id: int,
    data: StaffLeaveCreate,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    return await service.create_staff_leave(
        current_user.id,
        staff_id,
        data,
    )


@router.get(
    "/me/staff/{staff_id}/leave",
    response_model=list[StaffLeaveResponse],
)
async def get_staff_leave(
    staff_id: int,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    return await service.get_staff_leaves(
        current_user.id,
        staff_id,
    )