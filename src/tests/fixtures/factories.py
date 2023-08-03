from factory import DictFactory, Faker

from utils.users import make_hashed_password


class UserFactory(DictFactory):
    email: str = Faker('email')
    hashed_password: str = make_hashed_password('strongPassword1')
    verified: bool = True
    is_superuser: bool = True
    is_moderator: bool = True


class UserLoginFactory(DictFactory):
    email: str = Faker('email')
    password: str = 'strongPassword1'


class UserSignUpFactory(DictFactory):
    email: str = Faker('email')
    password: str = 'strongPassword1'
    password_confirm: str = 'strongPassword1'


class UserPasswordNotMatchFactory(DictFactory):
    email: str = Faker('email')
    password: str = 'strongPassword1'
    password_confirm: str = 'strongPassword2'
