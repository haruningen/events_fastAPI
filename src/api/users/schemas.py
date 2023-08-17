from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

__all__ = ('UserBaseSchema', 'TokenPayload', 'VerifyEmailSchema', 'OTPSchema', 'OTPEnableResponseSchema',)


class UserBaseSchema(BaseModel):
    email: EmailStr
    avatar_url: Optional[str]
    tfa_enabled: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class TokenPayload(BaseModel):
    user_id: Optional[int] = None
    exp: Optional[int] = None


class VerifyEmailSchema(BaseModel):
    email_verified_hash: str


class OTPEnableResponseSchema(BaseModel):
    otp_auth_url: str


class OTPSchema(BaseModel):
    otp_code: Optional[str] = None
