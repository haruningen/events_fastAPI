from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text

from config import settings
from models.base import BaseModel
from utils.images import remove_image, save_image, save_image_by_url


class User(BaseModel):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(45), index=True, unique=True)
    hashed_password: str = Column(String(1024), index=True, unique=True)
    verified: bool = Column(Boolean, nullable=False, server_default='False')
    created_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    avatar_path: str = Column(String(255))
    tfa_secret: str = Column(String(32), index=True, unique=True)
    tfa_enabled: bool = Column(Boolean, nullable=False, server_default='False')
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_moderator: bool = Column(Boolean, default=False, nullable=False)

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

    async def set_avatar_path_by_url(self, image: str) -> None:
        path = await save_image_by_url(
            image=image,
            name=f'{datetime.utcnow().timestamp()}_{self.id}',  # UTC timestamp + user ID
            path=settings.AVATARS_DIR
        )
        await remove_image(f'{settings.AVATARS_DIR}/{self.avatar_path}')
        self.avatar_path = path
