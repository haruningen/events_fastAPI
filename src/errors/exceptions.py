from fastapi.exceptions import ValidationException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

__all__ = (
    'unexpected_exceptions_handler',
)


async def unexpected_exceptions_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, ValidationException):
        detail = [str(e) for e in exc.errors()]
    else:
        detail = ['Unexpected error']

    return JSONResponse({'detail': detail}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)
