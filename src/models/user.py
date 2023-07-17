from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import TIMESTAMP, Boolean, Column, String, text

from models.base import BaseModel


class User(SQLAlchemyBaseUserTableUUID, BaseModel):
    __tablename__ = 'users'

    email: Column = Column(String(45), index=True, unique=True)
    avatar_url: Column = Column(String, nullable=True)
    verified: Column = Column(Boolean, nullable=False, server_default='False')
    created_at: Column = Column(TIMESTAMP(timezone=True),
                                nullable=False, server_default=text("now()"))
    updated_at: Column = Column(TIMESTAMP(timezone=True),
                                nullable=False, server_default=text("now()"))
