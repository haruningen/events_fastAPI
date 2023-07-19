from email.header import Header

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from connections.postgresql import async_session, db
from models import User
from utils.users import token_decode, get_user_by_email, get_user_by_id
from fastapi import HTTPException, status


async def get_db() -> AsyncSession:
    db = async_session()
    try:
        yield db
    finally:
        await db.close()


async def get_authed_user(token: str = Header(None, header_name='Authorization')) -> User:
    token_data = token_decode(token)
    user = await get_user_by_id(token_data.user_id)
    # Check if the user exist
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User with this email does not exist')
    yield user
