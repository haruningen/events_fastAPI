from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from common.auth import oauth2_scheme
from connections.postgresql import async_session
from models import User
from utils.users import token_decode


async def get_db() -> AsyncGenerator:
    db: AsyncSession = async_session()
    try:
        yield db
    finally:
        await db.close()


async def get_authed_user(token: str = Depends(oauth2_scheme)) -> User:
    token_data = token_decode(token)
    user = await User.get(token_data.user_id)  # type: ignore[func-returns-value]
    # Check if the user exist
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User with this email does not exist')
    return user
