from fastapi_users_db_sqlalchemy import GUID, UUID_ID, SQLAlchemyBaseOAuthAccountTableUUID
from sqlalchemy import Column, ForeignKey

from models.base import BaseModel


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, BaseModel):
    __tablename__ = 'oauth_accounts'

    user_id: UUID_ID = Column(GUID, ForeignKey('users.id', ondelete='cascade'), nullable=False)
