from uuid import uuid4

import sqlalchemy as sa
from fastapi import APIRouter, HTTPException, status

__all__ = ('router',)

from api.auth.schemas import CreateUserSchema, UserResponse
from models.user import User
from connections import db
from utils.users import get_hashed_password

router = APIRouter()


@router.post('/signup', summary="Create new user", response_model=UserResponse)
async def create_user(data: CreateUserSchema):
    user = (await db.execute(sa.select(User).filter_by(email=data.email))).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
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


