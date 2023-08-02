from pydantic import BaseModel

__all__ = ('MessageSchema',)


class MessageSchema(BaseModel):
    message: str
