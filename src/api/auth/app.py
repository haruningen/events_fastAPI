from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

__all__ = ('router',)

from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.schemas import (
    CreateUserSchema,
    EmailSchema,
    LoginOTPSchema,
    LoginUserSchema,
    RefreshTokenSchema,
    ResetPasswordConfirmSchema,
    TokenSchema,
    UserResponse,
    UserTFAResponse
)
from api.depends import get_db
from api.schemas import MessageSchema
from models.user import User
from utils.mail import reset_password, verify_email
from utils.users import (
    get_user_by_email,
    get_user_from_reset_password_link,
    make_auth_tokens,
    make_hashed_password,
    token_decode,
    verify_otp,
    verify_password
)

router = APIRouter(tags=['auth'])


@router.post('/signup', summary='Create new user', response_model=UserResponse)
async def create_user(data: CreateUserSchema,
                      background_tasks: BackgroundTasks,
                      _db: AsyncSession = Depends(get_db)) -> User:
    user = await get_user_by_email(data.email)
    # Check if the user exist
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this email already exist'
        )
    user = await User.create(
        email=data.email,
        hashed_password=make_hashed_password(data.password)
    )
    background_tasks.add_task(verify_email, data.email)
    return user


@router.post('/login', summary='Login user by credentials or with TFA', response_model=TokenSchema | UserTFAResponse)
async def login(data: LoginUserSchema, _db: AsyncSession = Depends(get_db)) -> dict:
    user = await get_user_by_email(data.email)
    # Check if the user exist
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User with this email does not exist')
    # Check if user verified his email
    if not user.verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Please verify your email address')
    # Check if the password is valid
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    if user.tfa_enabled:
        return {'otp_required': True}

    return make_auth_tokens(str(user.id))


@router.post('/otp/login', summary='Create access and refresh tokens for user', response_model=TokenSchema)
async def login_otp(data: LoginOTPSchema, _db: AsyncSession = Depends(get_db)) -> dict:
    user = await get_user_by_email(data.email)
    if not user or (user and not user.verified or user.tfa_enabled):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Unauthorized')
    verify_otp(user.tfa_secret, data.otp_code)
    return make_auth_tokens(str(user.id))


@router.post('/refresh', summary='Refresh access and refresh tokens for user', response_model=TokenSchema)
async def refresh(data: RefreshTokenSchema, _db: AsyncSession = Depends(get_db)) -> dict:
    token_data = token_decode(data.refresh_token, False)
    user = await User.get(token_data.user_id)  # type: ignore[func-returns-value]
    # Check if the user exist
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User with this email does not exist')
    return make_auth_tokens(str(user.id))


@router.post('/verify_email', summary='For test sending email verification link')
async def send_verify_email(data: EmailSchema, background_tasks: BackgroundTasks) -> dict:
    background_tasks.add_task(verify_email, data.email)
    return {'message': 'Verify email link send to email'}


@router.post('/reset_password', summary='Send reset password link to user email', response_model=MessageSchema)
async def send_reset_password(data: EmailSchema, background_tasks: BackgroundTasks) -> dict:
    background_tasks.add_task(reset_password, data.email)
    return {'message': 'Reset password link sent to email'}


@router.post('/reset_password_confirm', summary='Confirm user reset password by hash', response_model=MessageSchema)
async def reset_password_confirm(data: ResetPasswordConfirmSchema, _db: AsyncSession = Depends(get_db)) -> dict:
    user = await get_user_from_reset_password_link(data.password_reset_hash)
    # Check if the user exist
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User with this email does not exist')
    await user.update(User.email == user.email, hashed_password=make_hashed_password(data.new_password))
    return {'message': 'Password Reset Done'}
