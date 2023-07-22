import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from api import router as api
from config import settings

app = FastAPI()

origins = [
    settings.FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.mount(
    path=str(settings.MEDIA_URL.path),
    app=StaticFiles(directory=str(settings.MEDIA_ROOT)),
    name='media'
)

app.include_router(api, prefix=str(settings.API_ROOT))

# if settings.ENVIRONMENT == 'LOCAL' and __name__ == '__main__':
if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
