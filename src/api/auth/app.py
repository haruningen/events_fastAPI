import time

import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException, status

__all__ = ('router',)

from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.schemas import (
    CreateUserSchema,
    LoginUserSchema,
    RefreshTokenSchema,
    TokenSchema,
    UserResponse
)
from api.depends import get_db
from models.user import User
from utils.users import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    token_decode,
    verify_password, get_user_by_email
)

router = APIRouter()


@router.post('/signup', summary='Create new user', response_model=UserResponse)
async def create_user(data: CreateUserSchema, _db: AsyncSession = Depends(get_db)) -> User:
    user = await get_user_by_email(data.email)
    # Check if the user exist
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this email already exist'
        )
    user = User(
        email=data.email,
        hashed_password=get_hashed_password(data.password),
    )
    _db.add(user)
    await _db.commit()
    await _db.refresh(user)
    return user


@router.post('/login', summary='Create access and refresh tokens for user', response_model=TokenSchema)
async def login(data: LoginUserSchema, _db: AsyncSession = Depends(get_db)) -> dict:
    user = await get_user_by_email(data.email)
    # Check if the user exist
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User with this email does not exist')
    # TODO implement when add email verification
    # # Check if user verified his email
    # if not user.verified:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail='Please verify your email address')

    # Check if the password is valid
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    return {'access_token': create_access_token(user.email), 'refresh_token': create_refresh_token(user.email)}


@router.post('/refresh', summary='Refresh access and refresh tokens for user', response_model=TokenSchema)
async def refresh(data: RefreshTokenSchema, _db: AsyncSession = Depends(get_db)) -> dict:
    token_data = token_decode(data.refresh_token)
    user = await get_user_by_email(token_data.user_email)
    # Check if the user exist
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User with this email does not exist')
    return {'access_token': create_access_token(user.email), 'refresh_token': create_refresh_token(user.email)}
