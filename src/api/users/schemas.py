from typing import Optional

from pydantic import BaseModel, EmailStr

__all__ = ('UserBaseSchema', 'TokenPayload', 'VerifyEmailSchema' )


class UserBaseSchema(BaseModel):
    email: EmailStr
    avatar_url: Optional[str]

    class Config:
        orm_mode = True


class TokenPayload(BaseModel):
    user_id: Optional[str] = None
    exp: Optional[int] = None


class VerifyEmailSchema(BaseModel):
    email_verified_hash: str