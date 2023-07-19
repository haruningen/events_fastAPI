import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, constr, model_validator

from api.users.schemas import UserBaseSchema

__all__ = (
'CreateUserSchema', 'LoginUserSchema', 'UserResponse', 'TokenSchema', 'RefreshTokenSchema', 'EmailSchema')


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    password_confirm: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'CreateUserSchema':
        if self.password != self.password_confirm:
            raise ValueError('Passwords do not match')
        return self


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class EmailSchema(BaseModel):
    email: EmailStr


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class UserResponse(UserBaseSchema):
    id: uuid.UUID
    created_at: datetime
