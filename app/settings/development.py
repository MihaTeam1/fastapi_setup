from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware

from models.utils import Database

origins = [
    'http://localhost',
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    ),
]

settings = {
    'middleware': middleware,
}

database = Database(
    db_driver='postgresql+asyncpg',
    db_user='admin',
    db_pass='admin',
    db_host='127.0.0.1',
    db_port=5432,
    db_name='fastapi',
)