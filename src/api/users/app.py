from typing import Annotated

import jwt
import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException, status

from connections import db

__all__ = ('router',)

from pydantic import ValidationError

from api.users.schemas import TokenPayload, UserBaseSchema
from common.auth import oauth2_scheme
from config import settings
from models import User

router = APIRouter()

@router.get('/me', summary="Get current user info", response_model=UserBaseSchema)
async def get_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
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
    return user
