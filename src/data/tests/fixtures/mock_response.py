import json
from types import TracebackType
from typing import Optional, Type


class MockResponse:
    def __init__(self, text: str, status: int) -> None:
        self._text = text
        self.status = status

    async def text(self) -> str:
        return self._text

    async def __aexit__(
            self,
            xc_type: Optional[Type[BaseException]],
            exc: Optional[BaseException],
            tb: Optional[TracebackType],
    ) -> None:
        pass

    async def __aenter__(self) -> 'MockResponse':
        return self

    async def json(self) -> dict:
        return json.loads(self._text)
