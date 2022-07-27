from fastapi import Request, status
from fastapi.responses import JSONResponse, PlainTextResponse

from jose.exceptions import ExpiredSignatureError

from .exceptions import ValidationError


def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=[
            {
                'loc': ['body', msg[0]] if isinstance(msg, tuple) else 'body',
                'msg': msg[1] if isinstance(msg, tuple) else msg,
                'type': 'validation_error'
            }
            for msg in exc
        ],
        headers=exc.headers if hasattr(exc, 'headers') else None
    )


def expired_signature_error_handler(request: Request, exc: ExpiredSignatureError):
    return PlainTextResponse(
        'Token has been expired',
        status_code=status.HTTP_403_FORBIDDEN,
    )