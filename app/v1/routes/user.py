from fastapi.routing import APIRoute
from v1 import get_user, create_user

routes = [
    APIRoute('/create_user', endpoint=create_user, methods=['POST']),
    APIRoute('/{username}', endpoint=get_user)
]

__all__ = [
    'routes'
]