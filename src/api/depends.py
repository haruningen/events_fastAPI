from sqlalchemy.ext.asyncio import AsyncSession

from connections.postgresql import async_session


async def get_db() -> AsyncSession:
    db = async_session()
    try:
        yield db
    finally:
        await db.close()
