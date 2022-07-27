from fastapi import Request, status
from fastapi.responses import JSONResponse, PlainTextResponse
import logging

from jose.exceptions import ExpiredSignatureError

from .exceptions import ValidationError

logger = logging.getLogger(__name__)


def validation_error_handler(request: Request, exc: ValidationError):
    content = [
        {
            'loc': ['body', msg[0]] if isinstance(msg, tuple) else 'body',
            'msg': msg[1] if isinstance(msg, tuple) else msg,
            'type': 'validation_error'
        }
        for msg in exc
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=content,
        headers=exc.headers if hasattr(exc, 'headers') else None
    )


def expired_signature_error_handler(request: Request, exc: ExpiredSignatureError):
    return PlainTextResponse(
        'Token has been expired',
        status_code=status.HTTP_403_FORBIDDEN,
    )