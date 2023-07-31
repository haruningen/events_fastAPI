import uuid
from typing import Any, Optional, TypeVar, Union

from sqlalchemy import Column, ColumnCollection, MetaData, Select, select, update
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import declarative_base

from config import settings

__all__ = ('Base', 'DeclarativeBase', 'async_engine', 'async_session')

DeclarativeBaseType = TypeVar('DeclarativeBaseType', bound='DeclarativeBase')


class DeclarativeBase:

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.metadata: MetaData = MetaData()
        super().__init__(*args, **kwargs)

    @classmethod
    def _columns(cls) -> ColumnCollection:
        data: Any = inspect(cls)
        return data.columns

    @classmethod
    def _columns_keys(cls) -> list[str]:
        return [str(c.key) for c in cls._columns()]

    @classmethod
    def _pk_name(cls) -> str:
        data: Any = inspect(cls)
        return data.primary_key[0].name

    @classmethod
    def _pk_column(cls) -> Column:
        return getattr(cls, cls._pk_name())

    @property
    def _pk_value(self) -> Union[int, uuid.UUID]:
        return getattr(self, self._pk_name())

    @classmethod
    def _get_db(cls) -> AsyncSession:
        return async_session()

    @classmethod
    async def exec(
            cls, query: Select, _db: Optional[AsyncSession] = None
    ) -> Result:
        """Execute provided select query."""

        db: AsyncSession = _db or cls._get_db()
        try:
            result = await db.execute(query)
        finally:
            if not _db:
                await db.close()

        return result

    @classmethod
    async def create(
            cls,
            _db: Optional[AsyncSession] = None,
            _commit: bool = True,
            _refresh: bool = True,
            **kwargs: Any
    ) -> DeclarativeBaseType:
        """Create a new model instance and saves to DB."""

        db: AsyncSession = _db or cls._get_db()
        try:
            obj = cls.__call__(**kwargs)
            db.add(obj)

            if _commit:
                await db.commit()
                if _refresh:
                    await db.refresh(obj)
        finally:
            if not _db:
                await db.close()

        return obj

    @classmethod
    async def update(
            cls,
            *args: Any,
            _db: Optional[AsyncSession] = None,
            _commit: bool = True,
            **values: Any
    ) -> None:
        """Update model by satisfied query params."""

        db: AsyncSession = _db or cls._get_db()
        try:
            query = update(cls).where(*args).values(**values)

            await db.execute(query)

            if _commit:
                await db.commit()
        finally:
            if not _db:
                await db.close()

    @classmethod
    async def get(cls, pk: Any, _db: Optional[AsyncSession] = None) -> Optional[DeclarativeBaseType]:
        """Return a model instance by PK."""

        db: AsyncSession = _db or cls._get_db()
        try:
            obj = await db.get(cls, ident=pk)
        finally:
            if not _db:
                await db.close()

        return obj  # type: ignore[return-value]

    @classmethod
    async def exists_select(cls, query: Select, _db: Optional[AsyncSession] = None) -> bool:
        """Return existence result for provided query."""

        db: AsyncSession = _db or cls._get_db()
        try:
            result = await cls.exec(query.exists().select(), _db=db)
        finally:
            if not _db:
                await db.close()
        return result.scalar()  # type: ignore[return-value]

    @classmethod
    async def first(
            cls, _db: Optional[AsyncSession] = None, **kwargs: Any
    ) -> DeclarativeBaseType:
        """Return a first row."""

        db: AsyncSession = _db or cls._get_db()
        try:
            result = await db.execute(select(cls).filter_by(**kwargs))
        finally:
            if not _db:
                await db.close()

        return result.scalars().first()  # type: ignore[return-value]

    async def save(
            self,
            update_fields: Optional[Union[tuple[str, ...], list[str], set[str]]] = None,
            _db: Optional[AsyncSession] = None,
            _commit: bool = True,
    ) -> None:
        """Save changed model's fields to DB."""

        if not self._pk_value:
            raise Exception(
                f'Unable to get primary key value for {self} column {self._pk_column()}'
            )

        _columns_keys = self._columns_keys()
        if update_fields:
            data = {k: getattr(self, k) for k in _columns_keys if k in update_fields}
        else:
            data = {k: getattr(self, k) for k in _columns_keys}

        db: AsyncSession = _db or self._get_db()
        try:
            query = update(self.__class__).values(**data).where(
                self._pk_column() == self._pk_value
            )
            query.execution_options(synchronize_session='fetch')
            await db.execute(query)

            if _commit:
                await db.commit()
        finally:
            if not _db:
                await db.close()

    async def delete(self, _db: Optional[AsyncSession] = None, _commit: bool = True) -> None:
        """Delete a model instance from DB."""

        db: AsyncSession = _db or self._get_db()
        try:
            await db.delete(self)

            if _commit:
                await db.commit()
        finally:
            if not _db:
                await db.close()


Base: DeclarativeBase = declarative_base(cls=DeclarativeBase)

async_engine = create_async_engine(settings.POSTGRES_DSN)

async_session = async_sessionmaker(bind=async_engine, class_=AsyncSession, future=True, expire_on_commit=False)
