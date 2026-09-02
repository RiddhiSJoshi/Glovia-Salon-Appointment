from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User
from app.models.salon_model import Salon, Staff, Service, Appointment, Review


class AdminRepository:

    @staticmethod
    async def get_users(
        db: AsyncSession,
    ):
        result = await db.execute(
            select(User).order_by(User.id.desc())
        )

        return result.scalars().all()

    @staticmethod
    async def get_user_by_id(
        db: AsyncSession,
        user_id: int,
    ):
        result = await db.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def update_user(
        db: AsyncSession,
        user: User,
    ):
        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def delete_user(
        db: AsyncSession,
        user: User,
    ):
        await db.delete(user)
        await db.commit()

    @staticmethod
    async def count_users(db: AsyncSession):
        result = await db.execute(
            select(func.count(User.id))
        )

        return result.scalar_one()

    @staticmethod
    async def count_customers(db: AsyncSession):
        result = await db.execute(
            select(func.count(User.id))
            .where(User.role == "customer")
        )

        return result.scalar_one()

    @staticmethod
    async def count_salon_owners(db: AsyncSession):
        result = await db.execute(
            select(func.count(User.id))
            .where(User.role == "salon")
        )

        return result.scalar_one()

    @staticmethod
    async def count_admins(db: AsyncSession):
        result = await db.execute(
            select(func.count(User.id))
            .where(User.role == "admin")
        )

        return result.scalar_one()

    @staticmethod
    async def count_salons(db: AsyncSession):
        result = await db.execute(
            select(func.count(Salon.id))
        )

        return result.scalar_one()

    @staticmethod
    async def count_staff(db: AsyncSession):
        result = await db.execute(
            select(func.count(Staff.id))
        )

        return result.scalar_one()

    @staticmethod
    async def count_services(db: AsyncSession):
        result = await db.execute(
            select(func.count(Service.id))
        )

        return result.scalar_one()

    @staticmethod
    async def count_appointments(db: AsyncSession):
        result = await db.execute(
            select(func.count(Appointment.id))
        )

        return result.scalar_one()

    @staticmethod
    async def count_reviews(db: AsyncSession):
        result = await db.execute(
            select(func.count(Review.id))
        )

        return result.scalar_one()