from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salon_model import Review


class ReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ========================================================
    # CREATE
    # ========================================================

    async def create(
        self,
        customer_id: int,
        salon_id: int,
        rating: int,
        comment: str | None = None,
    ) -> Review:

        review = Review(
            customer_id=customer_id,
            salon_id=salon_id,
            rating=rating,
            comment=comment,
        )

        self.db.add(review)

        await self.db.commit()
        await self.db.refresh(review)

        return review

    # ========================================================
    # GET BY ID
    # ========================================================

    async def get_by_id(
        self,
        review_id: int,
    ) -> Review | None:

        result = await self.db.execute(
            select(Review).where(
                Review.id == review_id
            )
        )

        return result.scalar_one_or_none()

    # ========================================================
    # GET CUSTOMER REVIEW FOR SALON
    # ========================================================

    async def get_customer_salon_review(
        self,
        customer_id: int,
        salon_id: int,
    ) -> Review | None:

        result = await self.db.execute(
            select(Review).where(
                Review.customer_id == customer_id,
                Review.salon_id == salon_id,
            )
        )

        return result.scalar_one_or_none()

    # ========================================================
    # GET ALL SALON REVIEWS
    # ========================================================

    async def get_salon_reviews(
        self,
        salon_id: int,
    ) -> list[Review]:

        result = await self.db.execute(
            select(Review)
            .where(Review.salon_id == salon_id)
            .order_by(Review.id.desc())
        )

        return list(result.scalars().all())

    # ========================================================
    # UPDATE
    # ========================================================

    async def update(
        self,
        review: Review,
        rating: int | None = None,
        comment: str | None = None,
    ) -> Review:

        if rating is not None:
            review.rating = rating

        if comment is not None:
            review.comment = comment

        await self.db.commit()
        await self.db.refresh(review)

        return review

    # ========================================================
    # DELETE
    # ========================================================

    async def delete(
        self,
        review: Review,
    ) -> None:

        await self.db.delete(review)
        await self.db.commit()