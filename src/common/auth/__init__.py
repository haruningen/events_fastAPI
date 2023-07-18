from fastapi.security import OAuth2PasswordBearer

__all__ = ('oauth2_scheme',)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/login',
    scheme_name='JWT'
)