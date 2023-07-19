from connections.postgresql import Base, DeclarativeBase

__all__ = ('BaseModel',)


class BaseModel(Base, DeclarativeBase):  # type: ignore
    __abstract__ = True
    __tablename__ = ''