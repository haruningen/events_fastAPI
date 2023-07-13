from pydantic import BaseModel, EmailStr

__all__ = ('UserBaseSchema',)


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr
    avatar_url: str

    class Config:
        orm_mode = True
