from pydantic import BaseModel

__all__ = ('BaseMessageSchema',)


class BaseMessageSchema(BaseModel):
    message: str
