from typing import AsyncGenerator, TypeVar

T = TypeVar('T')

YieldAsyncFixture = AsyncGenerator[T, None]
