from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator

__all__ = (
    'ParsedEventTicketmasterSchema', 'ParsedEventPredictHQSchema',
    'TicketmasterConfigSchema', 'PredictHQConfigSchema'
)

from config import settings


class ParsedEventBaseSchema(BaseModel):
    name: str
    summary: str = ''
    image_path: Optional[str] = None
    source_id: str
    online_event: bool = False
    start: Optional[datetime] = None
    end: Optional[datetime] = None


class TicketmasterConfigSchema(BaseModel):
    size: int = settings.DATA_HANDLER_PER_PAGE
    load_images: bool = True


class PredictHQConfigSchema(BaseModel):
    limit: int = settings.DATA_HANDLER_PER_PAGE


class ParsedEventTicketmasterSchema(ParsedEventBaseSchema):
    source: str = 'ticketmaster'

    @model_validator(mode='before')
    def process_data(cls, data: dict) -> dict:
        new_data: dict = {
            'online_event': data.get('place') is None,
            'source_id': data['id'],
            'name': data['name']
        }
        if data.get('image_path'):
            new_data['image_path'] = data['image_path']
        if data.get('info'):
            new_data['summary'] = data['info']
        if data.get('description'):
            new_data['summary'] = data['description']
        if data['dates'].get('start'):
            if data['dates']['start'].get('dateTime'):
                new_data['start'] = datetime.strptime(data['dates']['start']['dateTime'], '%Y-%m-%dT%H:%M:%SZ')
            if data['dates']['start'].get('localDate'):
                new_data['start'] = datetime.strptime(data['dates']['start']['localDate'], '%Y-%m-%d')
        if data['dates'].get('end'):
            if data['dates']['end'].get('dateTime'):
                new_data['end'] = datetime.strptime(data['dates']['end']['dateTime'], '%Y-%m-%dT%H:%M:%SZ')
            if data['dates']['end'].get('localDate'):
                new_data['end'] = datetime.strptime(data['dates']['end']['localDate'], '%Y-%m-%d')
        return new_data


class ParsedEventPredictHQSchema(ParsedEventBaseSchema):
    source: str = 'predicthq'

    @model_validator(mode='before')
    def process_data(cls, data: dict) -> dict:
        new_data: dict = {
            'online_event': data.get('location') is None,
            'source_id': data['id'],
            'name': data['title'],
            'summary': data['description'],
            'start': data['start'],
            'end': data['end'],
        }
        return new_data
