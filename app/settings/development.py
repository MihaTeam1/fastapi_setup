from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from dotenv import load_dotenv
from pathlib import Path
import os

from schemas.db import Database

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

dev_settings = {
    'middleware': middleware,
}

database = Database(
    db_driver='postgresql+asyncpg',
    db_user=os.environ.get('POSTGRES_USER'),
    db_pass=os.environ.get('POSTGRES_PASSWORD'),
    db_host=os.environ.get('POSTGRES_HOST'),
    db_port=os.environ.get('POSTGRES_PORT'),
    db_name=os.environ.get('POSTGRES_DB'),
    echo=True,
    future=True,
)