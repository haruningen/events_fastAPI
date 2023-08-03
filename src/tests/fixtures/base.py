from datetime import datetime as dt

import pytest

__all__ = ('dt_iso',)


@pytest.fixture
def dt_iso() -> str:
    return dt.now().isoformat()
