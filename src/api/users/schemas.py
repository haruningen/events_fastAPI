from typing import Optional

from pydantic import BaseModel, EmailStr

__all__ = ('UserBaseSchema',)


class UserBaseSchema(BaseModel):
    email: EmailStr
    avatar_url: Optional[str]

    class Config:
        orm_mode = True
