from sqlalchemy import TIMESTAMP, Column, String, text
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from models.base import BaseModel


class User(SQLAlchemyBaseUserTableUUID, BaseModel):
    __tablename__ = 'users'

    email: Column = Column(String(45), index=True, unique=True)
    avatar_url: Column = Column(String, nullable=True)
    created_at: Column = Column(TIMESTAMP(timezone=True),
                                nullable=False, server_default=text("now()"))
    updated_at: Column = Column(TIMESTAMP(timezone=True),
                                nullable=False, server_default=text("now()"))
