from fastapi.security import OAuth2PasswordBearer

__all__ = ('oauth2_scheme',)

# TODO fix swagger auth
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/auth/login',
    scheme_name='JWT'
)