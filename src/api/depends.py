from typing import Annotated, AsyncGenerator

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from connections.postgresql import async_session
from models import User
from utils.users import token_decode

__all__ = (
    'get_db',
    'get_authed_user',
    'Pagination',
    'PaginationDeps',
    'valid_content_length',
    'verify_token',
)

_10_MB = (1024 * 1024) * 10  # 10 Mb size limit


async def get_db() -> AsyncGenerator:
    db: AsyncSession = async_session()
    try:
        yield db
    finally:
        await db.close()


async def get_authed_user(
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
) -> User:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Unauthorized')
    token_data = token_decode(token.credentials)
    user = await User.get(token_data.user_id)  # type: ignore[func-returns-value]
    # Check if the user exist
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Unauthorized')
    return user


async def verify_token(
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
) -> None:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Unauthorized')
    token_decode(token.credentials)


async def valid_content_length(content_length: int = Header(..., lt=_10_MB)) -> int:
    return content_length


class Pagination:

    def __init__(self, page: int, page_size: int) -> None:
        self.page = page
        self.page_size = page_size

    @property
    def limit(self) -> int:
        return self.page_size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


async def pagination_parameters(page: int = 1, page_size: int = 20) -> Pagination:
    return Pagination(page, page_size)


PaginationDeps = Annotated[Pagination, Depends(pagination_parameters)]
