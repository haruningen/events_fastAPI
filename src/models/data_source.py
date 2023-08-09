from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from models.base import BaseModel


class DataSource(BaseModel):
    __tablename__ = 'data_source'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(32))
    handler: str = Column(String(1024))
    last_event_id: str = Column(String(1024))
    api_url: str = Column(String(1024))
    secret: str = Column(String(1024), nullable=True)
    config = Column(JSONB, nullable=True)