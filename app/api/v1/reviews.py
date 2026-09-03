from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies import get_current_user

from app.schemas.review_schema import (
    ReviewCreate,
    ReviewResponse,
    ReviewUpdate,
)

from app.services.review_service import ReviewService


router = APIRouter(
    tags=["Reviews"],
)


# ============================================================
# CREATE REVIEW
# ============================================================

@router.post(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    data: ReviewCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = ReviewService(db)

        review = await service.create_review(
            customer_id=current_user.id,
            data=data,
        )

        return review

    except HTTPException:
        raise

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to review this appointment.",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create review.",
        )


# ============================================================
# GET SALON REVIEWS
# ============================================================

@router.get(
    "/salons/{salon_id}",
    response_model=list[ReviewResponse],
    status_code=status.HTTP_200_OK,
)
async def get_salon_reviews(
    salon_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = ReviewService(db)

        return await service.get_salon_reviews(
            salon_id=salon_id
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve salon reviews.",
        )


# ============================================================
# UPDATE REVIEW
# ============================================================

@router.put(
    "/{review_id}",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
)
async def update_review(
    data: ReviewUpdate,
    review_id: int = Path(..., gt=0),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = ReviewService(db)

        review = await service.update_review(
            review_id=review_id,
            customer_id=current_user.id,
            data=data,
        )

        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found.",
            )

        return review

    except HTTPException:
        raise

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own review.",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update review.",
        )


# ============================================================
# DELETE REVIEW
# ============================================================

@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_review(
    review_id: int = Path(..., gt=0),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        service = ReviewService(db)

        deleted = await service.delete_review(
            review_id=review_id,
            customer_id=current_user.id,
        )

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found.",
            )

        return None

    except HTTPException:
        raise

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own review.",
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete review.",
        )