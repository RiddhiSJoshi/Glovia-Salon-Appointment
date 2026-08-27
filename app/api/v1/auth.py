from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import jwt

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
)
from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.refresh_tokens import RefreshToken
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    LogoutRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):

    service = AuthService(db)

    user = await service.register(data)

    return user

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):

    service = AuthService(db)

    user = await service.authenticate_user(
        data.username,
        data.password,
    )

    access_token = create_access_token(
        user_id=user.id,
        role=user.role.value,
    )

    refresh_token = create_refresh_token()

    refresh_token_record = RefreshToken(
        user_id=user.id,
        token_hash=hash_refresh_token(
            refresh_token
        ),
        expires_at=(
            datetime.now(timezone.utc)
            + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )
        ),
        revoked=False,
    )

    db.add(refresh_token_record)

    await db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )

@router.post(
    "/refresh",
    response_model=TokenResponse,
)
async def refresh_token(
    data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):

    token_hash = hash_refresh_token(
        data.refresh_token
    )

    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token_hash == token_hash
        )
    )

    stored_token = result.scalar_one_or_none()

    if not stored_token:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    if stored_token.revoked:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked",
        )

    if stored_token.expires_at <= datetime.now(
        timezone.utc
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        )

    result = await db.execute(
        select(User).where(
            User.id == stored_token.user_id
        )
    )

    user = result.scalar_one_or_none()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    # Rotate refresh token
    stored_token.revoked = True

    new_access_token = create_access_token(
        user_id=user.id,
        role=user.role.value,
    )

    new_refresh_token = create_refresh_token()

    new_refresh_record = RefreshToken(
        user_id=user.id,
        token_hash=hash_refresh_token(
            new_refresh_token
        ),
        expires_at=(
            datetime.now(timezone.utc)
            + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )
        ),
        revoked=False,
    )

    db.add(new_refresh_record)

    await db.commit()

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )

@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    data: LogoutRequest,
    db: AsyncSession = Depends(get_db),
):

    token_hash = hash_refresh_token(
        data.refresh_token
    )

    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token_hash == token_hash
        )
    )

    stored_token = result.scalar_one_or_none()

    if stored_token:
        stored_token.revoked = True

        await db.commit()

    return None

@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_current_user_profile(
    current_user: User = Depends(
        get_current_user
    ),
):

    return current_user