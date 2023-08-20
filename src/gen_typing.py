from typing import AsyncGenerator, TypeVar

T = TypeVar('T')

YieldAsync = AsyncGenerator[T, None]
