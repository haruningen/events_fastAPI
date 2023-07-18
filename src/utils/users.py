from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
from pydantic import ValidationError

from api.users.schemas import TokenPayload
from config import settings
from connections import db
from models import User
import sqlalchemy as sa

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: str) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {'exp': expires_delta, 'user_email': str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: str) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {'exp': expires_delta, 'user_email': str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def token_decode(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Token signature has expired', )
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate credentials', )


async def get_user_by_email(email: str) -> User | None:
    users = (await db.execute(sa.select(User).filter_by(email=email))).first()
    if users:
        return users[0]
    else:
        return None
