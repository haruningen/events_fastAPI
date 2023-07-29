from pathlib import Path
from typing import Optional

import pyotp
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.depends import get_authed_user, get_db, valid_content_length

__all__ = ('router',)

from api.schemas import BaseMessageSchema
from api.users.schemas import UserBaseSchema, VerifyEmailSchema, OTPSchema
from config import settings
from models import User
from utils.users import get_user_from_email_link, verify_otp

router = APIRouter(tags=['users'])


@router.get('/me', summary='Get current user info', response_model=UserBaseSchema)
async def get_user(user: User = Depends(get_authed_user)) -> User:
    return user


@router.post('/me/avatar', dependencies=[Depends(valid_content_length)], tags=['users'])
async def upload_user_avatar(
        image: UploadFile = File(...), user: User = Depends(get_authed_user)
) -> dict[str, Optional[str]]:
    ext = Path(image.filename).suffix.lower()  # type: ignore[arg-type]
    if ext not in settings.IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Unsupported image type'
        )

    try:
        await user.set_avatar_path(image=image)
    finally:
        await user.save(['avatar_path'])
        await image.close()

    return {'avatar_url': user.avatar_url}


@router.post('/validate-email-token', summary='Verify user email by hash', response_model=BaseMessageSchema)
async def validate_email_confirm(verify_email: VerifyEmailSchema, _db: AsyncSession = Depends(get_db)) -> dict:
    user: Optional[User] = await get_user_from_email_link(verify_email.email_verified_hash)
    # Check if the user exist
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User with this email does not exist')
    if user.verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email Verification Failed. Email already verified.')
    await user.update(User.email == user.email, verified=True)
    return {'message': 'Email Verification Done'}


@router.post('/otp/enable')
async def enable_tfa(data: OTPSchema, user: User = Depends(get_authed_user)) -> dict:
    if user.tfa_enabled:
        verify_otp(user.tfa_secret, data.otp_code)
    tfa_secret = pyotp.random_base32()
    otp_auth_url = pyotp.totp.TOTP(tfa_secret).provisioning_uri(
        name=user.email, issuer_name='events.com')
    await user.update(User.email == user.email, tfa_secret=tfa_secret, tfa_enabled=True)
    return {'otp_auth_url': otp_auth_url}


@router.post('/otp/disable')
async def disable_tfa(data: OTPSchema, user: User = Depends(get_authed_user)) -> dict:
    if user.tfa_enabled:
        verify_otp(user.tfa_secret, data.otp_code)
    await user.update(User.email == user.email, tfa_secret=None, tfa_enabled=False)
    return {'message': '2-Step Verification Removed Successfully'}
