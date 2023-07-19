from email.header import Header

import sqlalchemy as sa
from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.auth import oauth2_scheme
from connections.postgresql import async_session, db
from models import User
from utils.users import get_user_by_email, get_user_by_id, token_decode


async def get_db() -> AsyncSession:
    db = async_session()
    try:
        yield db
    finally:
        await db.close()


async def get_authed_user(token: str = Depends(oauth2_scheme)) -> User:
    token_data = token_decode(token)
    user = await get_user_by_id(token_data.user_id)
    # Check if the user exist
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User with this email does not exist')
    return user
