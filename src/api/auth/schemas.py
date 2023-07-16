import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, constr, model_validator

from api.users.schemas import UserBaseSchema

__all__ = ('CreateUserSchema', 'LoginUserSchema', 'UserResponse', 'TokenSchema',)


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    passwordConfirm: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'CreateUserSchema':
        password = self.password
        passwordConfirm = self.passwordConfirm
        if password is not None and passwordConfirm is not None and password != passwordConfirm:
            raise ValueError('Passwords do not match')
        return self


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class RefreshTokenSchema(BaseModel):
    refresh_token: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class UserResponse(UserBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
