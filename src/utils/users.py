from datetime import datetime, timedelta
from typing import Any, Optional

import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
from pydantic import ValidationError

from api.users.schemas import TokenPayload
from config import settings
from models import OAuthAccount, User
from utils import cryptography

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
    user: User = await User.first(email=email)
    if user:
        return user
    else:
        return None


async def get_user_oauth(oauth_name: str, account_id: str) -> Optional[OAuthAccount]:
    user: OAuthAccount = await OAuthAccount.first(oauth_name=oauth_name, account_id=account_id)
    if user:
        return user
    else:
        return None


async def get_user_from_email_link(email_hash: str) -> Optional[User]:
    data = cryptography.decrypt_json(email_hash, settings.EMAIL_VERIFY_KEY)
    return await get_user_by_email(data['user_email'])


async def get_user_from_reset_password_link(reset_password_hash: str) -> Optional[User]:
    data = cryptography.decrypt_json(reset_password_hash, settings.RESET_PASSWORD_KEY)
    return await get_user_by_email(data['user_email'])
