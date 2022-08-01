from fastapi import Depends

from .token import verify_token


def auth_required(data: dict = Depends(verify_token)):
    pass