import asyncio
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

from config import settings


async def create_database(url: str) -> None:
    url_object = make_url(url)
    database_name = url_object.database
    dbms_url = url_object.set(database='postgres')
    engine = create_async_engine(dbms_url, isolation_level='AUTOCOMMIT')

    async with engine.connect() as conn:
        c = await conn.execute(
            text(f'SELECT 1 FROM pg_database WHERE datname={database_name!r}')
        )
        database_exists = c.scalar() == 1

    if database_exists:
        await drop_database(str(url_object))

    async with engine.connect() as conn:
        await conn.execute(
            text(f'CREATE DATABASE "{database_name}" ENCODING "utf8" TEMPLATE template1')
        )
    await engine.dispose()


async def drop_database(url: str) -> None:
    url_object = make_url(url)
    dbms_url = url_object.set(database='postgres')
    engine = create_async_engine(dbms_url, isolation_level='AUTOCOMMIT')
    async with engine.connect() as conn:
        disc_users = '''
        SELECT pg_terminate_backend(pg_stat_activity.%(pid_column)s)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '%(database)s'
          AND %(pid_column)s <> pg_backend_pid();
        ''' % {
            'pid_column': 'pid',
            'database': url_object.database,
        }
        await conn.execute(text(disc_users))

        await conn.execute(text(f'DROP DATABASE "{url_object.database}"'))


async def refresh_db() -> None:
    await drop_database(settings.POSTGRES_DSN)
    print('DB dropped')
    await create_database(settings.POSTGRES_DSN)
    print('DB created')

    # Remove migrations
    for m in Path('./migrations/versions').glob('*.py'):
        m.unlink(missing_ok=True)
    print('Migrations removed')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(refresh_db())
