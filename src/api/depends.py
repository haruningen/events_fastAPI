from email.header import Header

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from connections.postgresql import async_session
from models import User
from utils.users import get_user_by_email, token_decode


async def get_db() -> AsyncSession:
    db = async_session()
    try:
        yield db
    finally:
        await db.close()


async def get_authed_user(token: str = Header(None, header_name='Authorization')) -> User:
    token_data = token_decode(token)
    user = await get_user_by_email(token_data.user_email)
    # Check if the user exist
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    yield user
