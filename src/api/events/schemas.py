from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

__all__ = ('EventSchema', 'EventsListSchema',)


class EventSchema(BaseModel):
    id: int
    name: str
    summary: str
    image_url: Optional[str]
    online_event: Optional[bool]
    start: datetime
    end: datetime
    want_go: bool

    model_config = ConfigDict(from_attributes=True)


class EventsListSchema(BaseModel):
    items: list[EventSchema]
    count: int
