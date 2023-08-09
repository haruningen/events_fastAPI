import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from api import router as api
from data.tasks import load_data
from config import settings
from errors import unexpected_exceptions_handler

app = FastAPI()

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

@app.post("/tasks", status_code=201)
async def run_task():
    await load_data()

# if settings.ENVIRONMENT == 'LOCAL' and __name__ == '__main__':
if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
