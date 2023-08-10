from datetime import datetime
from typing import Optional

from aiohttp import ClientSession

from data.base import BaseDataHandler
from data.schemas import ParsedEventPredictHQSchema
from utils.images import save_image_by_url


class PredictHQDataHandler(BaseDataHandler):
    """
        The Strategy for get events from PredictHQ
    """

    async def to_event(self, data: dict) -> dict:
        schema = ParsedEventPredictHQSchema(**data)
        return schema.model_dump()

    async def get_events(self, session: ClientSession) -> Optional[list[dict]]:
        page = 0
        headers = {
            'Authorization': f'Bearer {self.ds.secret}'
        }
        params = {
            'active.gt': datetime.today().strftime('%Y-%m-%d'),
            'offset': page * self.ds.config['limit']
        }
        next_page = True

        while 3 > page and next_page:
            page += 1
            params['offset'] = page * self.ds.config['limit']
            if self.ds.config:
                params = self.ds.config | params
            res, next_page = await self.fetch_events(session, headers, params)

            for i in res:
                yield i

    async def fetch_events(self, session: ClientSession, headers: dict, params: dict) -> tuple[list[dict], bool]:
        events = list()
        async with session.get(self.ds.api_url, headers=headers, params=params) as response:
            fetch_data = await response.json()
            next_page = bool(fetch_data['next'])

            for event in fetch_data['results']:
                events.append(await self.to_event(event))

        return events, next_page
