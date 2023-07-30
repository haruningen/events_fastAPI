from typing import Optional
from sqlalchemy import Column, ForeignKey, String, Integer

from models.base import BaseModel


class OAuthAccount(BaseModel):
    __tablename__ = 'oauth_accounts'

    id: int = Column(Integer, primary_key=True)
    oauth_name: str = Column(String(length=100), index=True, nullable=False)
    access_token: str = Column(String(length=1024), nullable=False)
    expires_at: Optional[int] = Column(Integer, nullable=True)
    refresh_token: Optional[str] = Column(String(length=1024), nullable=True)
    account_id: str = Column(String(length=320), index=True, nullable=False)
    account_email: str = Column(String(length=320), nullable=False)
    user_id: int = Column(Integer, ForeignKey('users.id', ondelete='cascade'), nullable=False)
