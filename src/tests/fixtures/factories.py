from datetime import datetime
from typing import Optional

from factory import DictFactory, Faker

from utils.users import make_hashed_password


class UserFactory(DictFactory):
    email: str = Faker('email')
    hashed_password: str = make_hashed_password('strongPassword1')
    verified: bool = True
    is_superuser: bool = True
    is_moderator: bool = True
    tfa_secret: Optional[str] = None
    tfa_enabled: bool = False


class EventFactory(DictFactory):
    name: str = 'Test'
    summary: str = 'test summary'
    start: datetime = datetime.now()
