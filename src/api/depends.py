from typing import AsyncGenerator

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from connections.postgresql import async_session
from models import User
from utils.users import token_decode

__all__ = ('get_db', 'get_authed_user', 'valid_content_length')

_10_MB = (1024 * 1024) * 10  # 10 Mb size limit


async def get_db() -> AsyncGenerator:
    db: AsyncSession = async_session()
    try:
        yield db
    finally:
        await db.close()


async def get_authed_user(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> User:
    token_data = token_decode(token.credentials)
    user = await User.get(token_data.user_id)  # type: ignore[func-returns-value]
    # Check if the user exist
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User with this email does not exist')
    return user


async def valid_content_length(content_length: int = Header(..., lt=_10_MB)) -> int:
    return content_length
