from typing import Annotated

import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.depends import get_db

__all__ = ('router',)

from api.users.schemas import UserBaseSchema
from common.auth import oauth2_scheme
from models import User
from utils.users import token_decode

router = APIRouter()


@router.get('/me', summary='Get current user info', dependencies=[Depends(token_decode)], response_model=UserBaseSchema)
async def get_user(token: str = Depends(oauth2_scheme), _db: AsyncSession = Depends(get_db)) -> User:
    token_data = token_decode(token)
    user = (await _db.execute(sa.select(User).filter_by(email=token_data.user_email))).first()[0]
    # Check if the user exist
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    return user
