from sqlalchemy import Column, ForeignKey, Integer

from models.base import BaseModel


class UserEvent(BaseModel):
    __tablename__ = 'users_events'

    user_id: int = Column(Integer, ForeignKey('users.id'), primary_key=True)
    event_id: int = Column(Integer, ForeignKey('events.id'), primary_key=True)
