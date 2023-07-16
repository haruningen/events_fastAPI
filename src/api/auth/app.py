import time

import jwt
import sqlalchemy as sa
from fastapi import APIRouter, HTTPException, status

__all__ = ('router',)

from pydantic import ValidationError

from api.auth.schemas import CreateUserSchema, LoginUserSchema, TokenSchema, UserResponse, RefreshTokenSchema
from api.users.schemas import TokenPayload
from config import settings
from connections import db
from models.user import User
from utils.users import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password
)

router = APIRouter()


@router.post('/signup', summary="Create new user", response_model=UserResponse)
async def create_user(data: CreateUserSchema):
    user = (await db.execute(sa.select(User).filter_by(email=data.email))).first()[0]
    # Check if the user exist
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    # Check if the passwords same
    if data.password != data.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords don't match"
        )
    user = User(
        email=data.email,
        hashed_password=get_hashed_password(data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(data: LoginUserSchema):
    user = (await db.execute(sa.select(User).filter_by(email=data.email))).first()[0]
    # Check if the user exist
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    # TODO implement when add email verification
    # # Check if user verified his email
    # if not user.verified:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail='Please verify your email address')

    # Check if the password is valid
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    return TokenSchema(access_token=create_access_token(user.email), refresh_token=create_refresh_token(user.email))


@router.post('/refresh', summary="Refresh access and refresh tokens for user", response_model=TokenSchema)
async def refresh(data: RefreshTokenSchema):
    try:
        payload = jwt.decode(
            data.refresh_token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Could not validate credentials", )
    user = (await db.execute(sa.select(User).filter_by(email=token_data.sub))).first()[0]
    # Check if the user exist
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    # Check token exp date
    if time.time() > token_data.exp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Refresh token is no longer valid')
    return TokenSchema(access_token=create_access_token(user.email), refresh_token=create_refresh_token(user.email))
