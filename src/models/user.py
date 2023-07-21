from datetime import datetime

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import TIMESTAMP, Boolean, Column, String, text
from sqlalchemy.orm import Mapped

from models.base import BaseModel


class User(SQLAlchemyBaseUserTableUUID, BaseModel):
    __tablename__ = 'users'

    email: Mapped[str] = Column(String(45), index=True, unique=True)
    avatar_url: Mapped[str] = Column(String, nullable=True)
    verified: Mapped[bool] = Column(Boolean, nullable=False, server_default='False')
    created_at: Mapped[datetime] = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at: Mapped[datetime] = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
