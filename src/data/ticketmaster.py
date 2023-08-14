from datetime import datetime
from typing import Optional

from aiohttp import ClientSession

from utils.images import save_image_by_url

from .base import BaseDataHandler
from .schemas import ParsedEventTicketmasterSchema


class TicketmasterDataHandler(BaseDataHandler):
    """
    The Strategy for get events from Ticketmaster
    """

    async def to_event(self, data: dict) -> dict:
        images_size = [i['width'] * i['height'] for i in data['images']]
        image = data['images'][images_size.index(max(images_size))]
        image_path = await save_image_by_url(
            image=image['url'],
            name=f'{datetime.utcnow().timestamp()}_{data["id"]}',  # UTC timestamp + user ID
        )
        schema = ParsedEventTicketmasterSchema(image_path=image_path, **data)
        return schema.model_dump()

    async def get_events(self, session: ClientSession) -> Optional[list[dict]]:  # type: ignore
        page = 0
        headers = {'Content-Type': 'application/json'}
        params = {
            'apikey': self.ds.secret,
            'endDateTime': datetime.today().strftime('%Y-%m-%d') + 'T23:59:00Z',
            'page': page
        }
        next_page = True

        while 3 > page and next_page:
            page += 1
            params['page'] = page
            if self.ds.config:
                params = self.ds.config | params
            res, next_page = await self.fetch_events(session, headers, params)

            for i in res:
                yield i

    async def fetch_events(self, session: ClientSession, headers: dict, params: dict) -> tuple[list[dict], bool]:
        events = list()
        async with session.get(self.ds.api_url, headers=headers, params=params) as response:
            fetch_data = await response.json()
            next_page = bool(fetch_data['_links'].get('next'))

            for event in fetch_data['_embedded']['events']:
                events.append(await self.to_event(event))

        return events, next_page
