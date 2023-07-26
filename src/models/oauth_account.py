from fastapi_users_db_sqlalchemy import SQLAlchemyBaseOAuthAccountTableUUID
from fastapi_users_db_sqlalchemy.generics import GUID

from sqlalchemy import Column, ForeignKey

from models.base import BaseModel


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, BaseModel):
    __tablename__ = 'oauth_accounts'

    user_id: GUID = Column(GUID, ForeignKey('users.id', ondelete='cascade'), nullable=False)
