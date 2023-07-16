from typing import Optional

from pydantic import BaseModel, EmailStr

__all__ = ('UserBaseSchema', 'TokenPayload',)


class UserBaseSchema(BaseModel):
    email: EmailStr
    avatar_url: Optional[str]

    class Config:
        orm_mode = True


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
