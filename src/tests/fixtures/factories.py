from datetime import datetime

from factory import DictFactory, Faker
from pyotp import random_base32

from utils.users import make_hashed_password


class UserFactory(DictFactory):
    email: str = Faker('email')
    hashed_password: str = make_hashed_password('strongPassword1')
    verified: bool = True
    is_superuser: bool = True
    is_moderator: bool = True


class UserTFAFactory(DictFactory):
    email: str = Faker('email')
    hashed_password: str = make_hashed_password('strongPassword1')
    verified: bool = True
    is_superuser: bool = True
    is_moderator: bool = True
    tfa_secret: str = random_base32()
    tfa_enabled: bool = True


class UserLoginFactory(DictFactory):
    email: str = Faker('email')
    password: str = 'strongPassword1'


class UserLoginTFAFactory(DictFactory):
    email: str = Faker('email')
    password: str = 'strongPassword1'
    tfa_secret: str = random_base32()


class UserSignUpFactory(DictFactory):
    email: str = Faker('email')
    password: str = 'strongPassword1'
    password_confirm: str = 'strongPassword1'


class UserPasswordNotMatchFactory(DictFactory):
    email: str = Faker('email')
    password: str = 'strongPassword1'
    password_confirm: str = 'strongPassword2'


class EventFactory(DictFactory):
    name: str = 'Test'
    summary: str = 'test summary'
    start: datetime = datetime.now()
