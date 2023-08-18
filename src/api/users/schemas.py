from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

__all__ = ('UserBaseSchema', 'VerifyEmailSchema', 'OTPSchema', 'OTPEnableResponseSchema',)


class UserBaseSchema(BaseModel):
    email: EmailStr
    avatar_url: Optional[str]
    tfa_enabled: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class VerifyEmailSchema(BaseModel):
    email_verified_hash: str


class OTPEnableResponseSchema(BaseModel):
    otp_auth_url: str


class OTPSchema(BaseModel):
    otp_code: Optional[str] = None
