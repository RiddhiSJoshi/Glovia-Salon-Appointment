from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies import get_salon_owner

from app.schemas.staff_schema import (
    StaffCreate,
    StaffResponse,
    StaffUpdate,
)

from app.services.staff_service import StaffService


router = APIRouter(
    tags=["Salon Staff"],
)

@router.post(
    "/",
    response_model=StaffResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_staff(
    data: StaffCreate,
    salon_id: int = Path(..., gt=0),
    current_user=Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = StaffService(db)

        staff = await service.create_staff(
            salon_id=salon_id,
            owner_id=current_user.id,
            data=data,
        )

        return staff

    except HTTPException:
        raise

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to manage staff for this salon.",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create staff.",
        )

@router.get(
    "/",
    response_model=list[StaffResponse],
    status_code=status.HTTP_200_OK,
)
async def get_staff(
    salon_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
):
    """
    Public endpoint.

    Customers need this to select a stylist.
    """

    try:
        service = StaffService(db)

        return await service.get_staff_by_salon(
            salon_id=salon_id
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve staff.",
        )

@router.get(
    "/{staff_id}",
    response_model=StaffResponse,
    status_code=status.HTTP_200_OK,
)
async def get_staff_member(
    salon_id: int = Path(..., gt=0),
    staff_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = StaffService(db)

        staff = await service.get_staff(
            salon_id=salon_id,
            staff_id=staff_id,
        )

        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found.",
            )

        return staff

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve staff member.",
        )

@router.put(
    "/{staff_id}",
    response_model=StaffResponse,
    status_code=status.HTTP_200_OK,
)
async def update_staff(
    data: StaffUpdate,
    salon_id: int = Path(..., gt=0),
    staff_id: int = Path(..., gt=0),
    current_user=Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = StaffService(db)

        staff = await service.update_staff(
            salon_id=salon_id,
            staff_id=staff_id,
            owner_id=current_user.id,
            data=data,
        )

        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found.",
            )

        return staff

    except HTTPException:
        raise

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this staff member.",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update staff member.",
        )

@router.delete(
    "/{staff_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_staff(
    salon_id: int = Path(..., gt=0),
    staff_id: int = Path(..., gt=0),
    current_user=Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = StaffService(db)

        deleted = await service.delete_staff(
            salon_id=salon_id,
            staff_id=staff_id,
            owner_id=current_user.id,
        )

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found.",
            )

        return None

    except HTTPException:
        raise

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this staff member.",
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete staff member.",
        )