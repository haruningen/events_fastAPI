from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

Base = declarative_base()

async_engine = create_async_engine(settings.POSTGRES_DSN)

async_session = sessionmaker(bind=async_engine, class_=AsyncSession, future=True, expire_on_commit=False)

db = async_session()
