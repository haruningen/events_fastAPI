from connections.postgresql import Base, DeclarativeBase

__all__ = ('BaseModel',)


class BaseModel(Base, DeclarativeBase):
    __abstract__ = True
    __tablename__ = ''
