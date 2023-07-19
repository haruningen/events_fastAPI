from datetime import datetime, timedelta
from typing import Any, Optional

import jwt
import sqlalchemy as sa
from fastapi import HTTPException, status
from fastapi_users_db_sqlalchemy import UUID_ID
from passlib.context import CryptContext
from pydantic import ValidationError

from api.users.schemas import TokenPayload
from config import settings
from connections import db
from models import User

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def make_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def make_token(expire_minutes: int, secret_key: str, data: dict[str, Any]) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode = {'exp': expires_delta, **data}
    encoded_jwt = jwt.encode(to_encode, secret_key, settings.ALGORITHM)
    return encoded_jwt


def make_auth_tokens(user_id: str) -> dict:
    return {
        'access_token': make_token(settings.ACCESS_TOKEN_EXPIRE_MINUTES,
                                   settings.JWT_SECRET_KEY,
                                   {'user_id': user_id}),
        'refresh_token': make_token(settings.REFRESH_TOKEN_EXPIRE_MINUTES,
                                    settings.JWT_REFRESH_SECRET_KEY,
                                    {'user_id': user_id})
    }


def token_decode(token: str, is_access: bool = True) -> TokenPayload:
    secret_key = settings.JWT_SECRET_KEY if is_access else settings.JWT_REFRESH_SECRET_KEY
    try:
        payload = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Token signature has expired', )
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate credentials', )


async def get_user_by_email(email: str) -> Optional[User]:
    users = (await db.execute(sa.select(User).filter_by(email=email))).first()
    return users[0] if users else None


# TODO remove when merge with BaseClass for DB
async def get_user_by_id(user_id: str) -> Optional[User]:
    users = (await db.execute(sa.select(User).filter_by(id=user_id))).first()
    return users[0] if users else None
