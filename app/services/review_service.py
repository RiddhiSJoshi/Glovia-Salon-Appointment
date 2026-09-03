from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon_model import (Review,
    Appointment,
    AppointmentStatus,
)

from app.schemas.review_schema import (
    ReviewCreate,
    ReviewUpdate,
)

from app.repositories.review_repo import ReviewRepository


class ReviewService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = ReviewRepository(db)

    # ========================================================
    # CREATE REVIEW
    # ========================================================

    async def create_review(
        self,
        customer_id: int,
        data: ReviewCreate,
    ) -> Review:

        # ----------------------------------------------------
        # Check whether customer has completed appointment
        # at this salon
        # ----------------------------------------------------

        result = await self.db.execute(
            select(Appointment).where(
                Appointment.customer_id == customer_id,
                Appointment.salon_id == data.salon_id,
                Appointment.status == AppointmentStatus.COMPLETED,
            )
        )

        appointment = result.scalar_one_or_none()

        if not appointment:
            raise PermissionError(
                "You can only review a salon after completing an appointment."
            )

        # ----------------------------------------------------
        # Prevent duplicate review
        # ----------------------------------------------------

        existing_review = (
            await self.repository.get_customer_salon_review(
                customer_id=customer_id,
                salon_id=data.salon_id,
            )
        )

        if existing_review:
            raise ValueError(
                "You have already reviewed this salon."
            )

        # ----------------------------------------------------
        # Create review
        # ----------------------------------------------------

        return await self.repository.create(
            customer_id=customer_id,
            salon_id=data.salon_id,
            rating=data.rating,
            comment=data.comment,
        )

    # ========================================================
    # GET SALON REVIEWS
    # ========================================================

    async def get_salon_reviews(
        self,
        salon_id: int,
    ) -> list[Review]:

        return await self.repository.get_salon_reviews(
            salon_id=salon_id
        )

    # ========================================================
    # UPDATE REVIEW
    # ========================================================

    async def update_review(
        self,
        review_id: int,
        customer_id: int,
        data: ReviewUpdate,
    ) -> Review | None:

        review = await self.repository.get_by_id(
            review_id=review_id
        )

        if not review:
            return None

        # ----------------------------------------------------
        # Ownership check
        # ----------------------------------------------------

        if review.customer_id != customer_id:
            raise PermissionError(
                "You can only update your own review."
            )

        # ----------------------------------------------------
        # Nothing to update
        # ----------------------------------------------------

        if (
            data.rating is None
            and data.comment is None
        ):
            raise ValueError(
                "At least one field must be provided for update."
            )

        # ----------------------------------------------------
        # Update
        # ----------------------------------------------------

        return await self.repository.update(
            review=review,
            rating=data.rating,
            comment=data.comment,
        )

    # ========================================================
    # DELETE REVIEW
    # ========================================================

    async def delete_review(
        self,
        review_id: int,
        customer_id: int,
    ) -> bool:

        review = await self.repository.get_by_id(
            review_id=review_id
        )

        if not review:
            return False

        # ----------------------------------------------------
        # Ownership check
        # ----------------------------------------------------

        if review.customer_id != customer_id:
            raise PermissionError(
                "You can only delete your own review."
            )

        # ----------------------------------------------------
        # Delete
        # ----------------------------------------------------

        await self.repository.delete(review)

        return True