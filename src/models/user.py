from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import TIMESTAMP, Boolean, Column, String, text

from config import settings
from models.base import BaseModel
from utils.images import remove_image, save_image


class User(SQLAlchemyBaseUserTableUUID, BaseModel):
    __tablename__ = 'users'

    email: str = Column(String(45), index=True, unique=True)
    hashed_password: str = Column(String(1024), index=True, unique=True)
    verified: bool = Column(Boolean, nullable=False, server_default='False')
    created_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    avatar_path: str = Column(String(255))

    @property
    def avatar_url(self) -> Optional[str]:
        if not self.avatar_path:
            return None

        return f'{settings.MEDIA_URL}/{settings.AVATARS_DIR}/{self.avatar_path}'

    async def set_avatar_path(self, image: UploadFile) -> None:
        path = await save_image(
            image=image,
            name=f'{datetime.utcnow().timestamp()}_{self.id}',  # UTC timestamp + user ID
            path=settings.AVATARS_DIR
        )
        await remove_image(f'{settings.AVATARS_DIR}/{self.avatar_path}')
        self.avatar_path = path
