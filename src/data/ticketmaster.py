from datetime import datetime
from typing import Optional

from config import settings
from models import Event
from utils.images import save_image_by_url
from .base import BaseDataHandler
from aiohttp import ClientSession


class TicketmasterDataHandler(BaseDataHandler):
    """
    The Strategy for get events from Ticketmaster
    """

    async def to_event(self, data: dict) -> Event:
        summary = ''
        start = None
        end = None
        images_size = [i['width'] * i['height'] for i in data['images']]
        image = data['images'][images_size.index(max(images_size))]
        id = data['id']
        image_url = await save_image_by_url(
            image=image['url'],
            name=f'{datetime.utcnow().timestamp()}_{id}',  # UTC timestamp + user ID
        )
        if data.get('info'):
            summary = data['info']
        if data.get('description'):
            summary = data['description']
        if data['dates'].get('start'):
            if data['dates']['start'].get('dateTime'):
                start = datetime.strptime(data['dates']['start']['dateTime'], '%Y-%m-%dT%H:%M:%SZ')
            if data['dates']['start'].get('localDate'):
                start = datetime.strptime(data['dates']['start']['localDate'], '%Y-%m-%d')
        if data['dates'].get('end'):
            if data['dates']['end'].get('dateTime'):
                start = datetime.strptime(data['dates']['end']['dateTime'], '%Y-%m-%dT%H:%M:%SZ')
            if data['dates']['end'].get('localDate'):
                start = datetime.strptime(data['dates']['end']['localDate'], '%Y-%m-%d')
        return Event(
            name=data['name'],
            summary=summary,
            start=start,
            end=end,
            image_url=image_url,
            source_id=id,
            online_event=data.get('place') is None,
            source='ticketmaster'
        )

    # TODO with pages
    async def get_events(self, session: ClientSession) -> Optional[list[Event]]:
        events = list()
        _page = 0
        _headers = {'Content-Type': 'application/json'}
        _params = {'apikey': settings.TICKETMASTER_API_KEY,
                   'size': 1,
                   'endDateTime': datetime.today().strftime('%Y-%m-%d') + 'T23:59:00Z',
                   'page': _page}
        _totalPages = 0
        fetch_data = await self.fetch_events(session, _headers, _params)
        events.extend(fetch_data)
        while 3 > _page < _totalPages:
            _page += 1
            _params['page'] = _page
            fetch_data = await self.fetch_events(session, _headers, _params)
            events.extend(fetch_data)
        else:
            _page = -1
        return events

    async def fetch_events(self, session, _headers, _params) -> list[Event]:
        events = list()
        async with session.get(settings.TICKETMASTER_API_URL, headers=_headers, params=_params) as response:
            _fetch_data = await response.json()
            _totalPages = _fetch_data['page'].get('totalPages')
            for _event in _fetch_data['_embedded']['events']:
                events.append(await self.to_event(_event))
        return events
