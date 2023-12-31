from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from models.base import BaseModel


class DataSource(BaseModel):
    __tablename__ = 'data_source'

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(32), nullable=False)
    handler: str = Column(String(1024), nullable=False)
    api_url: str = Column(String(1024), nullable=False)
    secret: str = Column(String(1024), nullable=True)
    config: dict = Column(JSONB, nullable=False)
