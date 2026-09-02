import asyncio

from sqlalchemy import select

from app.db.database import AsyncSessionLocal
from app.core.security import hash_password
from app.models.user_model import User


async def seed_admin():
    async with AsyncSessionLocal() as db:
        # Check if admin already exists
        result = await db.execute(
            select(User).where(User.role == "admin")
        )
        existing_admin = result.scalar_one_or_none()

        if existing_admin:
            print("Admin already exists.")
            print(f"Username: {existing_admin.username}")
            return

        admin = User(
            username="admin",
            firstname="System",
            lastname="Admin",
            password_hash=hash_password("Admin@123"),
            role="admin",
        )

        db.add(admin)
        await db.commit()
        await db.refresh(admin)

        print("Admin created successfully!")
        print("Username: admin")
        print("Password: Admin@123")


if __name__ == "__main__":
    asyncio.run(seed_admin())