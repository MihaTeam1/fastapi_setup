from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .exceptions import ValidationError

def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content=[
            {
                'loc': ['body', msg[0]] if isinstance(msg, tuple) else 'body',
                'msg': msg[1] if isinstance(msg, tuple) else msg,
                'type': 'validation_error'
            }
            for msg in exc
        ]
    )