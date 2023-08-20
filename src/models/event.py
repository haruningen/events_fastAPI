from datetime import datetime
from typing import Optional

from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, UniqueConstraint, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, relationship

from config import settings
from models.base import BaseModel

from .user import User


class Event(BaseModel):
    __tablename__ = 'events'
    __table_args__ = (
        UniqueConstraint('source', 'source_id', name='ix_unique_source_source_id'),
    )

    id: int = Column(Integer, primary_key=True)
    created_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    name: str = Column(String(100))
    summary: str = Column(String(1000))
    image_path: str = Column(String(255))
    source: str = Column(String(100))
    source_id: str = Column(String(100))
    online_event: bool = Column(Boolean, nullable=False, server_default='False')
    start: datetime = Column(TIMESTAMP(timezone=True), nullable=True)
    end: datetime = Column(TIMESTAMP(timezone=True), nullable=True)

    users: Mapped[list[User]] = relationship('User', secondary='users_events', lazy='joined')

    @property
    def image_url(self) -> Optional[str]:
        if not self.image_path:
            return None

        return f'{settings.MEDIA_URL}/{self.image_path}'

    async def add_user(self, user: User, _db: AsyncSession) -> None:
        self.users.append(user)
        _db.add(self)
        await _db.commit()

    async def remove_user(self, user: User, _db: AsyncSession) -> None:
        self.users.remove(user)
        _db.add(self)
        await _db.commit()
