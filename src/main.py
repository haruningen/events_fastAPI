import uvicorn
from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from admin import AdminAuth, DataSourceAdmin, EventAdmin, UserAdmin
from api import router as api
from config import settings
from connections import async_engine
from data import load_data_task  # noqa
from errors import unexpected_exceptions_handler
from worker import celery  # noqa

app = FastAPI()

authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)

admin = Admin(app=app, engine=async_engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(EventAdmin)
admin.add_view(DataSourceAdmin)

origins = [
    settings.FRONTEND_URL,
]
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_exception_handler(Exception, unexpected_exceptions_handler)

app.mount(
    path=str(settings.MEDIA_URL.path),
    app=StaticFiles(directory=str(settings.MEDIA_ROOT)),
    name='media'
)

app.include_router(api, prefix=str(settings.API_ROOT))

# if settings.ENVIRONMENT == 'LOCAL' and __name__ == '__main__':
if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
