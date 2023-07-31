from factory import DictFactory, Faker

class UserLoginFactory(DictFactory):
    email: str = Faker('email')
    password: str = 'strongPassword1'

class UserFactory(DictFactory):
    email: str = Faker('email')
    password: str = 'strongPassword1'
    password_confirm: str = 'strongPassword1'

class UserPasswordNotMatchFactory(DictFactory):
    email: str = Faker('email')
    password: str = 'strongPassword1'
    password_confirm: str = 'strongPassword2'
