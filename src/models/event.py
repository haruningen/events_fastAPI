from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from models.base import BaseModel

from .user import User


class Event(BaseModel):
    __tablename__ = 'events'

    id: int = Column(Integer, primary_key=True)
    created_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    name: str = Column(String(100))
    summary: str = Column(String(1000))
    image_url: str = Column(String(255))
    source: str = Column(String(100))
    source_id: str = Column(String(100))
    online_event: bool = Column(Boolean, nullable=False, server_default='False')
    start: datetime = Column(TIMESTAMP(timezone=True), nullable=True)
    end: datetime = Column(TIMESTAMP(timezone=True), nullable=True)

    users: list[User] = relationship('User', secondary='users_events', lazy='joined')

    async def add_user(self, user: User, _db: AsyncSession) -> None:
        self.users.append(user)
        _db.add(self)
        await _db.commit()

    async def remove_user(self, user: User, _db: AsyncSession) -> None:
        self.users.remove(user)
        _db.add(self)
        await _db.commit()
