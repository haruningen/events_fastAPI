from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

__all__ = ('EventSchema', 'EventsListSchema', 'EventDetailScheme',)


class EventSchema(BaseModel):
    id: int
    name: str
    summary: str
    image_url: Optional[str]
    online_event: Optional[bool]
    start: Optional[datetime]
    end: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class EventDetailScheme(EventSchema):
    want_go: Optional[bool] = None


class EventsListSchema(BaseModel):
    items: list[EventSchema]
    count: int
