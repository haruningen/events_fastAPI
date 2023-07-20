import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, constr, model_validator, Field

from api.users.schemas import UserBaseSchema

__all__ = (
    'CreateUserSchema', 'LoginUserSchema', 'UserResponse', 'TokenSchema', 'RefreshTokenSchema', 'EmailSchema',
    'ResetPasswordConfirmSchema')


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    password_confirm: str

    @model_validator(mode='after') # type: ignore[misc]
    def check_passwords_match(self) -> 'CreateUserSchema':
        if self.password != self.password_confirm:
            raise ValueError('Passwords do not match')
        return self # type: ignore[return-value]


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


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


class ResetPasswordConfirmSchema(BaseModel):
    password_reset_hash: str
    new_password: str = Field(min_length=8)
    re_new_password: str

    @model_validator(mode='after') # type: ignore[misc]
    def check_passwords_match(self) -> 'ResetPasswordConfirmSchema':
        if self.new_password != self.re_new_password:
            raise ValueError('Passwords do not match')
        return self # type: ignore[return-value]
