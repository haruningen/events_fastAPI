from sqladmin import ModelView

from models import User


class UserAdmin(ModelView, model=User):
    icon = 'fa-solid fa-user'

    column_list = [
        User.id, User.email, User.verified, User.tfa_enabled, User.is_moderator, User.is_superuser
    ]
