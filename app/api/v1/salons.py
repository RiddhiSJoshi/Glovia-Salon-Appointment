from fastapi import APIRouter, Depends, status, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.user_model import User
from app.schemas.salon_schema import (
    SalonCreate,
    SalonUpdate,
    SalonResponse,
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse
)
from app.services.salon_service import SalonService
from app.core.security import get_current_user
from app.dependencies import get_salon_owner


router = APIRouter(
    tags=["Salon Management"],
)


@router.post(
    "/",
    response_model=SalonResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_salon(
    data: SalonCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Create a salon for the authenticated salon owner.
    """

    try:
        service = SalonService(db)

        salon = await service.create_salon(
            owner_id=current_user.id,
            data=data,
        )

        return {
            "message": "Salon created successfully!",
            "salon": salon
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create salon.",
        )


@router.get(
    "/",
    response_model=SalonResponse,
    status_code=status.HTTP_200_OK,
)
async def get_my_salon(
    current_user=Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    """
    Get the salon belonging to the authenticated salon owner.
    """

    try:
        service = SalonService(db)

        salon = await service.get_salon_by_owner(
            owner_id=current_user.id
        )

        if not salon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salon not found for the current owner.",
            )

        return salon

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve salon.",
        )



@router.get(
    "/{salon_id}",
    response_model=SalonResponse,
    status_code=status.HTTP_200_OK,
)
async def get_salon(
    salon_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
):
    """
    Public endpoint.
    Customers can view salon information.
    """

    try:
        service = SalonService(db)

        salon = await service.get_salon(salon_id)

        if not salon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salon not found.",
            )

        return salon

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve salon.",
        )


@router.put(
    "/{salon_id}",
    response_model=SalonResponse,
    status_code=status.HTTP_200_OK,
)
async def update_salon(
    data: SalonUpdate,
    salon_id: int = Path(..., gt=0),
    current_user=Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    """
    Update salon information.

    Only the owner of the salon can update it.
    """

    try:
        service = SalonService(db)

        salon = await service.update_salon(
            salon_id=salon_id,
            owner_id=current_user.id,
            data=data,
        )

        if not salon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salon not found.",
            )

        return {
            "message": "Salon updated successfully!",
            "salon": salon
        }

    except HTTPException:
        raise

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this salon.",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update salon.",
        )


@router.delete(
    "/{salon_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_salon(
    salon_id: int = Path(..., gt=0),
    current_user=Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete/deactivate salon.
    """

    try:
        service = SalonService(db)

        deleted = await service.delete_salon(
            salon_id=salon_id,
            owner_id=current_user.id,
        )

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salon not found.",
            )

        return {
            "message": "Salon deleted successfully!"
        }

    except HTTPException:
        raise

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this salon.",
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete salon.",
        )


# =====================================================
# CATEGORY
# =====================================================

@router.post(
    "/{salon_id}/categories",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    data: CategoryCreate,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    await service.create_category(
        current_user.id,
        data,
    )
    return {
        "message": "Category created successfully!"
    }


@router.get(
    "/{salon_id}/categories",
    response_model=list[CategoryResponse],
)
async def get_categories(
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    await service.get_categories(
        current_user.id
    )
    return {
        "message": "Categories fetched successfully!"
    }


@router.put(
    "/{salon_id}/categories/{category_id}",
    response_model=CategoryResponse,
)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    current_user: User = Depends(get_salon_owner),
    db: AsyncSession = Depends(get_db),
):
    service = SalonService(db)

    await service.update_category(
        current_user.id,
        category_id,
        data,
    )

    return {
        "message": "Category updated successfully!"
    }


@router.delete(
    "/{salon_id}/categories/{category_id}",
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
    return {
        "message": "Category deleted successfully!"
    }
