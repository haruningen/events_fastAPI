from connections.postgresql import Base

__all__ = ('BaseModel',)


class BaseModel(Base):  # type: ignore
    __abstract__ = True
    __tablename__ = ''