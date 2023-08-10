from connections.postgresql import Base, DeclarativeBase

__all__ = ('BaseModel',)


class BaseModel(Base, DeclarativeBase):
    __abstract__ = True
    __tablename__ = ''

    def __repr__(self) -> str:
        return f'{self.__tablename__}({getattr(self, "id")})'
