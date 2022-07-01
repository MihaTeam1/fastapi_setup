from fastapi import FastAPI
from .routes import routes
from .settings import settings

app = FastAPI(routes=routes, **settings)
