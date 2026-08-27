from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    hash_password,
    verify_password,
)
from app.models.user import User, UserRole
from app.repositories.auth_repo import AuthRepository
from app.schemas.auth import RegisterRequest


class AuthService:

    def __init__(self, db: AsyncSession):

        self.db = db

        self.repository = AuthRepository(db)

    async def register(
        self,
        data: RegisterRequest,
    ) -> User:

        username = data.username.strip().lower()

        existing_user = (
            await self.repository.get_user_by_username(
                username
            )
        )

        if existing_user:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username is already registered",
            )

        user = User(
            username=username,
            firstname=data.firstname.strip(),
            lastname=data.lastname.strip(),
            password_hash=hash_password(
                data.password
            ),
            role=UserRole.CUSTOMER,
            is_active=True,
        )

        return await self.repository.create_user(
            user
        )

    async def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> User:

        user = (
            await self.repository.get_user_by_username(
                username.strip().lower()
            )
        )

        if not user:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        if not verify_password(
            password,
            user.password_hash,
        ):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        if not user.is_active:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        return user